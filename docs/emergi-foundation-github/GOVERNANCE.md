# Emergi Foundation governance

The Emergi Foundation is a mission-driven open-science steward of
household-scale energy-equity tools. This document specifies how
decisions get made across the Foundation's open-source projects.

Governance-doc names DO include individual officers — see the
attribution policy in `CONTRIBUTING.md`.

## Mission

To alleviate energy poverty through community-led clean energy —
by publishing, maintaining, and citing open data and open-source
software for measuring energy burden, modelling household energy
footprint, and designing equitable transitions to clean energy.

## Organisational structure

The Foundation operates inside the broader **Emrgi** umbrella:
Emergi Cooperative (member-driven kWh accounting), Emergi Foundation
(this entity — 501(c)(3) OSS + research stewardship), and Emergi
Incorporated (community-solar product surface). The Foundation
holds all open-source assets, trademarks (where filed), and
citation identifiers for the ecosystem.

Legal-status note: 501(c)(3) status is asserted; formal
incorporation with an EIN and public board roster is on the
roadmap. Governance below applies from day zero; incorporation
elevates the same structure with legal enforceability.

## Steering committee

The Steering Committee is the Foundation's operational
decision-making body for open-source projects.

- **Composition**: at least 3 members from at least 2 organisations
  (target 6–12 members for sustainability).
- **Term**: 2 years, renewable.
- **Seats**: mix of project maintainers, external collaborators,
  and Foundation officers.
- **Chair**: elected by the committee for a 1-year term.

Current composition and appointment records live in
`STEERING_COMMITTEE.md` at repo root once a first slate is
seated. Until then the co-founders act as an interim committee.

## Decision-making

- **Lazy consensus** — proposals in issues or PRs move forward if
  no reasoned objection is raised in a stated review period
  (default 5 business days for code changes; 14 days for policy
  changes).
- **Vote** — used when lazy consensus fails or on major decisions
  (release cadence, license changes, major API breaks, trademark
  filings, budget). Simple majority of the steering committee;
  quorum = half rounded up.
- **Escalation** — the Chair adjudicates procedural questions.
  Substantive disagreement escalates to the full Steering
  Committee at its next scheduled meeting.

Meeting notes for policy-level decisions are recorded in a public
`decisions/` directory in the `.github` repo.

## Maintainer roles

Each package has a **Maintainer** (author with commit rights) and
optionally **Reviewers** (trusted contributors with review rights
but no commit). Maintainer identity is recorded in each repo's
`AUTHORS.md` and in `CODEOWNERS` where present.

Maintainers are responsible for:
- Reviewing and merging PRs consistent with the Foundation's
  attribution + naming policy (`CONTRIBUTING.md`).
- Cutting Mirror → Release tags per the ecosystem's publication
  workflow (`emburden-site/docs/PRIVATE_TO_PUBLIC.md`).
- Enforcing the Code of Conduct within their package's issues
  and PRs; escalating persistent violations to the CoC enforcement
  committee.

Adding a Maintainer to a package: proposed by an existing
Maintainer, ratified by lazy consensus in the Steering Committee.

## Code of Conduct enforcement

`CODE_OF_CONDUCT.md` sets the standards. Enforcement is by a
dedicated **CoC Enforcement Committee** of at least 3 members,
kept separate from any single package's maintainers. Reports go
to `conduct@emrgi.org`. Committee decisions are appealable to the
full Steering Committee within 30 days.

## License and IP policy

- All Foundation software is **AGPL-3.0-or-later** (or a
  compatible license inherited from an upstream fork).
- Contributions use the **DCO sign-off** convention. **No CLA**;
  **no copyright assignment**; contributors retain copyright.
- Trademark policy for the "Emergi" and "emburden" marks is in
  `TRADEMARK.md`. Trademarks (where registered) are held by the
  Foundation; the Foundation licenses them non-exclusively for
  fair use.

## Funding and financial transparency

Funding sources (if any) are disclosed in an annual transparency
report published at `emrgi.org/annual-report`. Grants received
through fiscal sponsors (NumFOCUS, Open Collective, Software
Freedom Conservancy) are itemised there.

Until the Foundation formally incorporates with an EIN, no direct
donations are accepted; the `FUNDING.yml` in each repo points at
fiscal-sponsor channels only.

## Amendments

This document is amended by Steering Committee vote (simple
majority, quorum = half rounded up). Amendments take effect at the
next release cycle.

## History

- 2026-09-19: initial version; interim steering by co-founders
  pending first seated committee.
