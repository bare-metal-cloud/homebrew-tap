# Formula for the CloudNative MySQL (cnms) kubectl plugin. GENERATED FILE:
# scripts/gen-formula.py rendered it from the cnms v0.4.2 release SHA256SUMS
# (the same digests the deploykit catalogue pins — NFR11). Do not edit by
# hand; rerun the generator or let the autoupdate workflow do it.
class KubectlCnms < Formula
  desc "Day-2 CLI for the CloudNative MySQL (cnms) operator"
  homepage "https://github.com/bare-metal-cloud/cnms"
  version "0.4.2"

  # The cnms repo is private today: the release URLs below only resolve with
  # authentication until the assets are mirrored to the public edge
  # (get.low-cost.cloud/dl/cnms/...). The sha256 pins are already final —
  # when the mirror lands, only the url host/path changes.
  on_macos do
    if Hardware::CPU.intel?
      url "https://github.com/bare-metal-cloud/cnms/releases/download/v0.4.2/kubectl-cnms_v0.4.2_darwin_amd64.tar.gz"
      sha256 "f61ccd2bb285c7e62655c56ebf0702b41a0712655b21856bc72ef821db41a10b"
    end
    if Hardware::CPU.arm?
      url "https://github.com/bare-metal-cloud/cnms/releases/download/v0.4.2/kubectl-cnms_v0.4.2_darwin_arm64.tar.gz"
      sha256 "8ee48858102b1353a822eb70a520c3b25c71b3dff3fd6f69e74539b286500b27"
    end
  end
  on_linux do
    if Hardware::CPU.intel?
      url "https://github.com/bare-metal-cloud/cnms/releases/download/v0.4.2/kubectl-cnms_v0.4.2_linux_amd64.tar.gz"
      sha256 "c782c2c62a5afec33b1b53c78b6db35bf6ae1d2a8b8e8af9ef70d3fedc3d59d2"
    end
    if Hardware::CPU.arm?
      url "https://github.com/bare-metal-cloud/cnms/releases/download/v0.4.2/kubectl-cnms_v0.4.2_linux_arm64.tar.gz"
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
