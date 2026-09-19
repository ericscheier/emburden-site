# Contributing to Emergi Foundation projects

Thanks for considering a contribution. This is the canonical
contribution policy for **all** projects under the
`emergi-foundation` GitHub org. Individual repos may add their own
`CONTRIBUTING.md` with repo-specific dev-setup notes on top of what
this document specifies.

## License

All Foundation projects are licensed **AGPL-3.0-or-later** (or a
compatible license, per each repo's `LICENSE` file). Contributions
are accepted under the same license. Contributions to non-AGPL
Foundation projects (e.g., `DeepSolar` inherits MIT from its
Stanford upstream) accept the project's stated license.

## Contributor certification (DCO, no CLA)

We use the [Developer Certificate of Origin](https://developercertificate.org/)
convention: by opening a pull request you certify that you have
the right to submit the contribution under the project license.
**No separate Contributor License Agreement.** No copyright
assignment: you retain copyright to your contributions.

`git commit -s` (sign-off) is welcomed. Bots enforce sign-off on
PRs that add nontrivial code.

## How to contribute

1. **Bug reports** at the specific package's Mirror-tier issue
   tracker (`github.com/ericscheier/<pkg>/issues`). Include the
   minimal reproducer, package version, R session info
   (`sessionInfo()`), and expected vs observed behaviour. Search
   open + closed issues first.
2. **Feature suggestions** at the same tracker with the
   `enhancement` label. Describe the underlying research question
   or workflow gap, not just the API you'd like.
3. **Pull requests** for code, docs, tests, or data-loader
   additions. Open an issue first for anything beyond a small fix
   so we can align on scope before you invest time.

Foundation-level policy and cross-cutting concerns
(publication workflow, gated-data handling, release cadence) are
documented at
[emburden-site/docs/PRIVATE_TO_PUBLIC.md](https://github.com/ericscheier/emburden-site/blob/master/docs/PRIVATE_TO_PUBLIC.md).

## Style

- R packages: tidyverse style guide; snake_case for functions,
  columns, variables; roxygen documentation with `@examples` on
  public functions.
- Comments in code only when the *why* is non-obvious. Well-named
  functions and clear code are preferred to running commentary.
- Tests under `tests/testthat/` following the `test-<module>.R`
  naming.

## Attribution and naming policy

Foundation projects use **role-based attribution** in public docs,
code, and rendered publications by default:

- Public docs (paper, site content, comments, docstrings) refer to
  the project ("emburden project"), the Foundation ("Emergi
  Foundation"), or the maintainer role ("project maintainer") —
  not named individuals.
- **Named-individual attribution is opt-in.** Contributors who
  want personal credit list themselves in the repo's `AUTHORS.md`.
- **Cited academic authors** in scholarly references are exempt
  — citation of published methods by author name is required for
  academic legibility.
- **Governance docs** (`GOVERNANCE.md`, the Foundation board list,
  the CoC enforcement committee roster) DO name officers — this
  is standard nonprofit practice and a separate genre from paper /
  site content.
- **AI-collaboration attribution** is documented at the project
  level in each repo's `AUTHORS.md`, not per-commit.

`git log` remains the authoritative raw record of who contributed
which lines.

## Security disclosures

Private disclosures go to `security@emrgi.org`. Do not open a
public issue for security problems. Response commitment: initial
acknowledgement within 5 business days, plan of action within 15.

## Trademark

Policy for the "Emergi", "Emergi Foundation", and "emburden" marks
is in `TRADEMARK.md`. Contributions do not grant a trademark
license.

## Governance

Foundation governance is documented in `GOVERNANCE.md`. Decisions
follow lazy consensus; escalations go to the steering committee.
