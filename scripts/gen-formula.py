#!/usr/bin/env python3
"""Regenerate Formula/kubectl-cnms.rb from a cnms release SHA256SUMS.

The formula's version, per-platform URLs and sha256 pins are derived
entirely from the release assets: the same SHA256SUMS the cnms release
pipeline uploads and the deploykit catalogue pins (NFR11 — one source of
truth). The formula file is fully generated; edit this script or feed it a
different SHA256SUMS, never the .rb by hand.

Usage:
    gen-formula.py --tag v0.4.2 --sums path/to/SHA256SUMS \
        [--repo bare-metal-cloud/cnms] [--out Formula/kubectl-cnms.rb]
"""

import argparse
import sys
from pathlib import Path

TEMPLATE = """\
# Formula for the CloudNative MySQL (cnms) kubectl plugin. GENERATED FILE:
# scripts/gen-formula.py rendered it from the cnms @TAG@ release SHA256SUMS
# (the same digests the deploykit catalogue pins — NFR11). Do not edit by
# hand; rerun the generator or let the autoupdate workflow do it.
class KubectlCnms < Formula
  desc "Day-2 CLI for the CloudNative MySQL (cnms) operator"
  homepage "https://github.com/@REPO@"
  version "@VER@"

  # Download transport: the cnms GitHub repo is private, so its release URLs
  # 404 anonymously. The formula downloads from the public edge instead
  # (get.low-cost.cloud/dl/cnms/...) — the deploykit mirror serves the
  # identical tarballs, so the sha256 pins below are the same
  # release-SHA256SUMS digests either way (issue #13). A version is
  # fetchable here only once the deploykit catalogue pins it; the digest
  # check fails loudly if the edge ever serves different bytes.
  on_macos do
    if Hardware::CPU.intel?
      url "https://get.low-cost.cloud/dl/cnms/@TAG@/darwin/amd64.tar.gz"
      sha256 "@DARWIN_AMD64@"
    end
    if Hardware::CPU.arm?
      url "https://get.low-cost.cloud/dl/cnms/@TAG@/darwin/arm64.tar.gz"
      sha256 "@DARWIN_ARM64@"
    end
  end
  on_linux do
    if Hardware::CPU.intel?
      url "https://get.low-cost.cloud/dl/cnms/@TAG@/linux/amd64.tar.gz"
      sha256 "@LINUX_AMD64@"
    end
    if Hardware::CPU.arm?
      url "https://get.low-cost.cloud/dl/cnms/@TAG@/linux/arm64.tar.gz"
      sha256 "@LINUX_ARM64@"
    end
  end

  # Each tarball contains a single kubectl-cnms binary; kubectl discovers it
  # on PATH as `kubectl cnms` (standard kubectl plugin mechanism).
  def install
    bin.install "kubectl-cnms"
  end

  test do
    assert_match "cnms plugin v#{version}", shell_output("#{bin}/kubectl-cnms version")
  end
end
"""

WANTED = [("linux", "amd64"), ("linux", "arm64"), ("darwin", "amd64"), ("darwin", "arm64")]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tag", required=True, help="release tag, e.g. v0.4.2")
    ap.add_argument("--sums", required=True, help="path to the release SHA256SUMS")
    ap.add_argument("--repo", default="bare-metal-cloud/cnms")
    ap.add_argument("--out", default="Formula/kubectl-cnms.rb")
    args = ap.parse_args()

    if not args.tag.startswith("v"):
        sys.exit(f"tag must look like v0.4.2, got {args.tag!r}")

    digests = {}
    for line in Path(args.sums).read_text().splitlines():
        if not line.strip():
            continue
        h, name = line.split(maxsplit=1)
        digests[name.strip().lstrip("*")] = h.strip()

    plat = {}
    for name, h in digests.items():
        if not (name.startswith("kubectl-cnms_") and name.endswith(".tar.gz")):
            continue
        stem = name[len("kubectl-cnms_") : -len(".tar.gz")]
        parts = stem.rsplit("_", 2)
        if len(parts) == 3 and parts[0] == args.tag:
            plat[(parts[1], parts[2])] = h

    missing = [p for p in WANTED if p not in plat]
    if missing:
        sys.exit(f"SHA256SUMS is missing platforms: {missing}; found {sorted(plat)}")

    body = TEMPLATE
    body = body.replace("@REPO@", args.repo)
    body = body.replace("@TAG@", args.tag)
    body = body.replace("@VER@", args.tag[1:])
    for key, pair in [
        ("@LINUX_AMD64@", ("linux", "amd64")),
        ("@LINUX_ARM64@", ("linux", "arm64")),
        ("@DARWIN_AMD64@", ("darwin", "amd64")),
        ("@DARWIN_ARM64@", ("darwin", "arm64")),
    ]:
        body = body.replace(key, plat[pair])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body)
    print(f"wrote {out} (cnms {args.tag}, 4 platform digests from {args.sums})")


if __name__ == "__main__":
    main()
