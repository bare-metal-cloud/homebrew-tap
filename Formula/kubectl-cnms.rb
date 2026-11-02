# Formula for the CloudNative MySQL (cnms) kubectl plugin. GENERATED FILE:
# scripts/gen-formula.py rendered it from the cnms v0.4.2 release SHA256SUMS
# (the same digests the deploykit catalogue pins — NFR11). Do not edit by
# hand; rerun the generator or let the autoupdate workflow do it.
class KubectlCnms < Formula
  desc "Day-2 CLI for the CloudNative MySQL (cnms) operator"
  homepage "https://github.com/bare-metal-cloud/cnms"
  version "0.4.2"

  # Download transport: the cnms GitHub repo is private, so its release URLs
  # 404 anonymously. The formula downloads from the public edge instead
  # (get.low-cost.cloud/dl/cnms/...) — the deploykit mirror serves the
  # identical tarballs, so the sha256 pins below are the same
  # release-SHA256SUMS digests either way (issue #13). A version is
  # fetchable here only once the deploykit catalogue pins it; the digest
  # check fails loudly if the edge ever serves different bytes.
  on_macos do
    if Hardware::CPU.intel?
      url "https://get.low-cost.cloud/dl/cnms/v0.4.2/darwin/amd64.tar.gz"
      sha256 "f61ccd2bb285c7e62655c56ebf0702b41a0712655b21856bc72ef821db41a10b"
    end
    if Hardware::CPU.arm?
      url "https://get.low-cost.cloud/dl/cnms/v0.4.2/darwin/arm64.tar.gz"
      sha256 "8ee48858102b1353a822eb70a520c3b25c71b3dff3fd6f69e74539b286500b27"
    end
  end
  on_linux do
    if Hardware::CPU.intel?
      url "https://get.low-cost.cloud/dl/cnms/v0.4.2/linux/amd64.tar.gz"
      sha256 "c782c2c62a5afec33b1b53c78b6db35bf6ae1d2a8b8e8af9ef70d3fedc3d59d2"
    end
    if Hardware::CPU.arm?
      url "https://get.low-cost.cloud/dl/cnms/v0.4.2/linux/arm64.tar.gz"
      sha256 "010c8ff5d933d8929e77044b19ff016acabdb26a1d89b0eaaaf8e0c762187d23"
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
