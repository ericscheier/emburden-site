# Emergi Foundation

**Alleviating energy poverty through community-led clean energy.**

The Emergi Foundation is a mission-driven open-science steward of
household-scale energy-equity tools. We publish, cite, and maintain
open datasets and open-source software for measuring energy burden,
modelling household energy footprint, and designing equitable
transitions to clean energy.

- Website: [emrgi.org](https://emrgi.org)
- Ecosystem home: [emburden.org](https://emburden.org)
- Contact: `info@emrgi.org`

The Foundation is part of the broader **Emrgi** umbrella
(Cooperative, Foundation, Incorporated). This GitHub org is the
Foundation's open-source publication home.

## Stewarded projects

### emburden ecosystem

The `emburden` R-package ecosystem — 14 packages covering data
loading (`emburdendata`), geographic utilities (`emburdengeo`),
statistical modelling (`emburdenstats`), utility workflows
(`emburdenutil`), climate + weather (`emburdenweather`), DERs +
solar (`emburdender`), health outcomes (`emburdenhealth`),
visualisation (`emburdenvis`), publication tooling
(`emburdenpub`), test infrastructure (`emburdentest`), the
meta-package (`emburdenplus`), the synthetic microdata pipeline
(`emburdensynth`), the emergy systems-language sub-package
(`energese`), and the core burden analysis (`emburden`).

Companion research site with paper drafts + atlas + methodology
lives at [emburden.org](https://emburden.org). The paper
"Where does emergy accounting give new information? A systematic
cross-country evaluation of 36 emergy-native metrics against 40
mainstream outcomes" is under active development.

### Standalone Foundation tools

- **`leroi`** — community-level energy-burden + EROI toolkit.
- **`Footprint`** — consumption-based carbon-footprint calculator.
- **`Efficiency`** — energy-usage efficiency assessment.
- **`EmergiPlan`** — Qualtrics-fed R/Shiny reporting.
- **`DeepSolar`** — nationwide solar-panel identification (fork,
  Stanford / wangzhecheng lineage).
- **`emjoule`** — Solidity ERC-1155 community-choice aggregation
  dApp.
- **`embit`** — Android smartphone energy meter (UNC undergrad
  lineage).
- **`reporting`** — sector reporting scaffolds.

## How we publish

Foundation repositories are the **canonical citable release
destination** for the emburden ecosystem. Working development
happens on private-then-public mirrors under personal orgs; tagged
releases land here with Zenodo DOIs, `CITATION.cff` metadata, and
license consistency. See the ecosystem's
[publication workflow doc](https://github.com/ericscheier/emburden-site/blob/master/docs/PRIVATE_TO_PUBLIC.md)
for the three-tier model (Dev → Mirror → Release).

## Contributing

See the org-level `CONTRIBUTING.md` for policy and the individual
package README for dev setup. The Foundation uses the DCO sign-off
convention (no CLA, no copyright assignment). Bug reports and PRs
go to the Mirror-tier repo of the specific package under
`github.com/ericscheier/`; releases mirror here on tag.

## Governance

The Foundation's charter, steering committee, and decision-making
process are documented in `GOVERNANCE.md`. Trademark policy for
the "Emergi" and "emburden" marks is in `TRADEMARK.md`. Code of
Conduct enforcement is by an independent committee — see
`CODE_OF_CONDUCT.md`.
