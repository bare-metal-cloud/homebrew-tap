# bare-metal-cloud/tap

Homebrew tap for bare-metal-cloud tooling. Currently installs:

- `kubectl-cnms` — the CloudNative MySQL (cnms) operator's day-2 CLI
  (`kubectl cnms status`, `promote`, `fencing`, backups/PITR, and more).

## Install

```sh
brew tap bare-metal-cloud/tap https://github.com/bare-metal-cloud/homebrew-tap
brew install bare-metal-cloud/tap/kubectl-cnms
kubectl cnms version
```

## Versions and digest provenance

Formulae here are machine-generated (`scripts/gen-formula.py`) from the cnms
release's own `SHA256SUMS` — the exact digest set the release pipeline
uploads and the deploykit catalogue (`bare-metal-cloud/catalog`) pins. One
release, one set of bytes, pinned everywhere (NFR11): brew, krew, the
deploykit rail, and manual curl installs all verify against the same
`SHA256SUMS`.

New versions land through the autoupdate workflow
(`.github/workflows/autoupdate.yml`):

- `workflow_dispatch` with input `version` (a release tag, e.g. `v0.4.2`), or
- `repository_dispatch` of type `plugin-release` with
  `client_payload.version` set to the tag — send it with:

  ```sh
  gh api repos/bare-metal-cloud/homebrew-tap/dispatches \
    -f event_type=plugin-release \
    -F 'client_payload[version]=v0.4.2'
  ```

The workflow downloads that release's plugin tarballs and `SHA256SUMS` from
`bare-metal-cloud/cnms`, verifies the downloads, regenerates the formula,
syntax-checks it, and commits `brew formula: v<version>`.

## Private-repo caveat

`bare-metal-cloud/cnms` is private today, so the formula's download URLs only
resolve with authentication until the release assets are mirrored to the
public edge (`get.low-cost.cloud/dl/cnms/...`). The sha256 pins are already
final — when the mirror lands, only the URL host/path changes (see the note
in `Formula/kubectl-cnms.rb`). The workflow needs a fine-grained PAT with
`Contents: Read` on `bare-metal-cloud/cnms` stored as the
`CNMS_RELEASE_TOKEN` secret; setup instructions are in the workflow's gate
step.
