# Emburden ecosystem: entities, orgs, and publication workflow

Single source of truth for **who** stewards the emburden ecosystem,
**where** the code lives, and **how** a change flows from a working
branch to a citable public release.

## The Emrgi entity tree

**Emrgi** is an umbrella brand over three related legal entities.
Per the `emrgi.com` footer: *"Emrgi is formed of the Emergi
Cooperative, the Emergi Foundation, and Emergi Incorporated."*

| Entity | Type | Public front-end |
|:---|:---|:---|
| **Emergi Cooperative** | Member cooperative (points-per-kWh; Energy Equity Fund with 1:1 match) | member-facing app under Emergi Inc. |
| **Emergi Foundation** | 501(c)(3) mission-driven nonprofit | `emrgi.org` |
| **Emergi Incorporated** | For-profit corp (community-solar / bill-smoothing product) | `emrgi.com` |

Co-founders: Eric Scheier, Karyn Miller. General contact:
`hello@emrgi.com`. Nonprofit contact: `info@emrgi.org`.

## Entity → GitHub org → role

| GitHub org | Legal entity | Role for the emburden ecosystem |
|:---|:---|:---|
| `ScheierVentures/*` | Personal LLC | **Dev tier** — private working repos. All day-to-day commits, WIP branches, gated-data caches. History rewrites allowed. |
| `ericscheier/*` | Personal user | **Mirror tier** — public WIP. External collaborators track this. Linear history; force-pushes disruptive. |
| `emergi-foundation/*` | Emergi Foundation (501c3) | **Release tier** — canonical citable home for tagged versions. Sibling to Foundation's existing tools: `leroi`, `Footprint`, `Efficiency`, `EmergiPlan`, `embit`. Zenodo community mints DOIs on tag. |
| `emrgi/*` | (research-adjacent scratch) | Existing fork mirror of energy-research tooling (pvlib, rdtools, PyPSA, etc.). **NOT the emburden release destination.** Kept as-is; may later host Emergi Inc. commercial code. |

Adjacent orgs `altfund/*` and `ominari-insights/*` are separate
lines of work (finance and prediction markets); out of scope for
the emburden ecosystem.

## What Emergi Foundation provides as steward

The Foundation is the publication and citation layer for the
ecosystem. It ships the following concretely, independent of
whether/when the 501(c)(3) status is formally incorporated with
an EIN:

- **Namespace + citable home** at
  `github.com/emergi-foundation/<pkg>` for every tagged release.
- **Zenodo community** ("Emergi Foundation") that mints a concept
  DOI (all versions) and a per-tag version DOI on every release.
  Wired via GitHub → Zenodo webhook on the Foundation org.
- **Org-level policy docs** in a single
  `emergi-foundation/.github` repo, inherited by every project:
  `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1),
  `CONTRIBUTING.md` (DCO sign-off, no CLA, no copyright
  assignment), `GOVERNANCE.md`, `TRADEMARK.md`, `SECURITY.md`,
  `FUNDING.yml`, `CITATION.cff` template, `profile/README.md`.
- **Trademark stewardship** for the "emburden" and "Emergi" marks
  (registration optional — usPTO ~$250–350 filing).
- **Umbrella JOSS meta-paper** naming all ecosystem packages;
  each package's `preferred-citation` field points to it.
- **ORCID-linked contributor registry** so authors appear
  consistently across DOIs and papers.
- **CoC enforcement committee** of ≥3 people from ≥2 orgs, kept
  separate from any single package's maintainers.
- **Fiscal-sponsorship track** for grant applications through
  NumFOCUS, Open Collective, or Software Freedom Conservancy —
  no self-incorporation required to accept grant funds.
- **Coordinated release calendar + shared reusable CI workflows**.

For **citation and DOI legitimacy**, the legal-form question
(formal 501(c)(3) vs asserted) doesn't matter — Zenodo, JOSS,
ORCID, and CrossRef only need a stable org identity and consistent
metadata. Legal form matters when the Foundation actually holds
funds, owns trademarks, or signs institutional grant contracts.

## Three-tier publication workflow

1. **Dev** at `ScheierVentures/*` (private): work happens here
   first. Feature branches, WIP, exploratory scripts. Push freely.
2. **Mirror** at `ericscheier/*` (public): every push of `main` /
   `global` / `ssa` etc. fans out via the `public` remote. External
   collaborators watch this. Linear history.
3. **Release** at `emergi-foundation/*` (public): tagged versions
   mirror here via a `release` remote added at first release. Only
   quality-gated tags land. Zenodo webhook mints DOIs automatically.

`git remote -v` at each repo shows the pattern (once wired):
```
scheier  git@github.com:ScheierVentures/<pkg>.git   (fetch/push)
public   git@github.com:ericscheier/<pkg>.git       (fetch/push)
release  git@github.com:emergi-foundation/<pkg>.git (push, tags only)
all      (points at scheier + public)               (fan-out push)
```

`git push all main` fans out Dev + Mirror on every push;
`git push release vX.Y.Z` pushes only tags to Release.

Cadence: Dev → Mirror continuous. Mirror → Release per tagged
version (monthly during active development, quarterly once API
stabilises).

## Per-release quality gate

Before mirroring a tag to Release:

- **Names**: grep code + docs for known collaborator names, personal
  emails, private handles. Replace with role-based labels ("emburden
  project", "external reviewer", "external collaborator"). Cited
  academic authors are exempt.
- **Secrets**: `git log -p --since='<prev-tag>' | grep -iE
  'secret|token|api_key|password'`.
- **Gated data**: confirm IEA WEB, DHS microdata, Afrobarometer +
  Latinobarómetro merged rounds, and any other gated caches are
  in `.gitignore` and behind env-var gates (e.g.,
  `IEA_LICENCE_ACKNOWLEDGED=true`).
- **Repo-root OSS files current**: `LICENSE`, `AUTHORS.md`,
  `CITATION.cff`, `CONTRIBUTING.md`, `.mailmap`.
- **R CMD check clean** for R packages.
- Tag: `git tag -a vX.Y.Z -m "release notes"`.
- Push to Release: `git push release vX.Y.Z`.
- Update `CITATION.cff` on Release with the version DOI once
  Zenodo mints it.

## Per-repo OSS files at Release tier

Each ecosystem repo carries at repo root:

- `LICENSE` — AGPL-3.0-or-later (ecosystem standard).
- `AUTHORS.md` — role-based, references Foundation stewardship,
  AI-collaboration disclosure at project level.
- `CONTRIBUTING.md` — points at
  `emergi-foundation/.github/CONTRIBUTING.md` for the canonical
  policy; per-repo carries only repo-specific dev-setup.
- `CITATION.cff` — role-based author "Emergi Foundation
  (`info@emrgi.org`)"; `repository-code:
  github.com/emergi-foundation/<pkg>` once first Release lands;
  Zenodo community `emergi-foundation`.
- `.zenodo.json` — Zenodo metadata (authors, ORCIDs, community
  slug, keywords).
- `.mailmap` — unactivated skeleton, ready to alias
  `eric@scheier.org` → `info@emrgi.org` when the transition ships.

On Release repos: **Issues + wiki disabled**; README banner points
at Mirror issue tracker at `github.com/ericscheier/<pkg>/issues`
to keep one canonical thread per package.

## Attribution + naming policy

- **Role-based attribution** ("emburden project", "Emergi
  Foundation") in public docs, code, and paper by default.
- **Named individuals opt in** via `AUTHORS.md` at repo root.
  Governance docs (Foundation board, steering committee) are a
  separate genre and DO name officers — normal nonprofit practice.
- **Cited academic authors** (Odum, Deming and Stephan, Hruschka
  et al., Reed and Jorgensen, etc.) are exempt from the naming
  policy: scholarly citation by author name is required for
  academic legibility.
- **No** `Co-Authored-By: Claude ...` **or** `Claude-Session: ...`
  **lines on commits going forward** (memory rule enforced at
  `~/.claude/projects/.../memory/feedback_no_claude_attribution.md`).
  AI-collaboration disclosure lives at project-level `AUTHORS.md`.
- **Historical commits keep their metadata** — no history rewrite.

## `emburden.org` attribution copy

Current footer says: *"emburden.org — an open project by Emrgi.
Data + code at github.com/ericscheier."*

New copy (recommended):
> emburden.org — an Emergi Foundation project.
> Code: github.com/emergi-foundation (releases) and
> github.com/ericscheier (working mirror).

## Executable checklist

**Codeable now** (in-session, no external accounts needed):

- [x] `emburden-site/docs/PRIVATE_TO_PUBLIC.md` — this document.
- [ ] `emburdensynth/AUTHORS.md` + `CONTRIBUTING.md` +
      `CITATION.cff` refreshed with explicit "Emergi Foundation"
      phrasing, Zenodo community, ORCID slot.
- [ ] `emburden-site/docs/emergi-foundation-github/*` — staged
      templates for the Foundation's org-defaults repo.
- [ ] `emburden-site` footer copy updated across Home, About,
      Papers pages.
- [ ] Template rollout to the 13 other ecosystem repos.

**User-gated** (GitHub UI + external services):

- [ ] Create `emergi-foundation/.github` org-defaults repo; push
      the staged templates.
- [ ] Create `emergi-foundation/emburdensynth` (empty) at first
      release; add `release` remote locally; push tags.
- [ ] Enable Zenodo → GitHub webhook on the Foundation org;
      create Zenodo community "Emergi Foundation".
- [ ] Optional: register "emburden" trademark (usPTO).
- [ ] Optional: apply to NumFOCUS Affiliated Project.
- [ ] Optional: file EIN + publish board roster for the
      Foundation to move from asserted to formal 501(c)(3).

## Non-goals

- **No history rewrite** of prior commits (destructive; disrupts
  external clones).
- **No org migration** — `ericscheier/*` stays as the Mirror tier;
  Release is a *separate destination for tagged versions*, not a
  move.
- **No formal incorporation** of Emergi Foundation as a 501(c)(3)
  in this arc — governance is aspirational-with-documentation
  until the user decides to file EIN + board.
- **No move of `emrgi/*`** — keep it as the research fork mirror.
- **No changes to `altfund/*` or `ominari-insights/*`** — separate
  lines of work.

## Change log

- 2026-09-19: Third and canonical version. First draft assumed a
  destination `emburden/*` org migration; corrected to
  `emergi-foundation/*` per its role as the nonprofit steward;
  this pass adds the full Emrgi entity tree context, distinguishes
  Foundation from Inc./Cooperative, and specifies the concrete
  stewardship deliverables and governance minimum-viable setup.
