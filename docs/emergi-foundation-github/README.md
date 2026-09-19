# Staged templates for `emergi-foundation/.github`

This directory holds the eight files that will become the
`emergi-foundation/.github` GitHub org-defaults repository once
the user creates it. The repo is a standard GitHub convention:
any file placed inside is inherited as the default for every
repo under the `emergi-foundation` org unless the repo overrides
it.

## Files staged here

| Local path | Target path in `emergi-foundation/.github` | Purpose |
|:---|:---|:---|
| `profile/README.md` | `profile/README.md` | The org profile page shown at `github.com/emergi-foundation` |
| `CODE_OF_CONDUCT.md` | `CODE_OF_CONDUCT.md` | Contributor Covenant 2.1 with enforcement contact |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` | DCO sign-off, PR flow, no CLA |
| `GOVERNANCE.md` | `GOVERNANCE.md` | Steering committee, decision-making, escalation |
| `TRADEMARK.md` | `TRADEMARK.md` | Policy for "emburden" / "Emergi" marks |
| `SECURITY.md` | `SECURITY.md` | Private-disclosure inbox |
| `FUNDING.yml` | `FUNDING.yml` | Funding channels shown in GitHub UI |
| `CITATION.cff` | `CITATION.cff` | Org-level citation template |

## To publish (user-gated)

1. Create the empty `emergi-foundation/.github` repository on
   GitHub (via web UI or `gh repo create`).
2. `git clone git@github.com:emergi-foundation/.github.git` and
   copy the eight files (preserving the `profile/` subdirectory
   for `profile/README.md`).
3. `git add . && git commit -m "Initial org defaults" && git push`.
4. Verify by visiting `github.com/emergi-foundation` — the
   `profile/README.md` should render as the org page.

## What each repo inherits

Every repo under `emergi-foundation/*` automatically shows the org
CoC, CONTRIBUTING, and SECURITY docs unless the repo has its own.
Per-repo `AUTHORS.md`, `CITATION.cff`, `README.md`, and `LICENSE`
still live inside each repo and override where present. This lets
per-package citation metadata coexist with org-level governance.
