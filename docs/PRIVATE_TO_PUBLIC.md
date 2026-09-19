# Ecosystem publication workflow

The emburden ecosystem uses a **three-tier hosting model** across
GitHub orgs: private working repo → public WIP mirror → foundation-
stewarded release. This document is the single source of truth for
which repo lives where and how a change flows from a working branch
to a public release.

## Three-tier hosting

| Tier | GitHub org | Visibility | Role |
|:---|:---|:---|:---|
| **Dev** | `ScheierVentures/*` | private | Working repo. All day-to-day commits land here first. History rewrites, force-pushes, WIP branches, credentials-in-transit all allowed. |
| **Mirror** | `ericscheier/*` | public | Early-access public mirror. External collaborators watch this. Continuous mirror from Dev, main branches only. History is expected to be linear here; force-pushes are disruptive. |
| **Release** | `emergi-foundation/*` | public | Foundation-stewarded canonical release. Tagged releases mirror here. This is the target for DOIs (Zenodo), CRAN, JOSS, and any external citation. |

Rationale:

- **Dev at `ScheierVentures`** keeps in-progress work private during
  the pre-release window. Contents include gated-data caches,
  API-key-adjacent secrets in `.env` files, exploratory scratch, and
  anything not yet ready to be public. AGPL-3.0-or-later still
  applies inside — the license does not depend on visibility — but
  no external clone happens until Mirror.
- **Mirror at `ericscheier`** is the public collaboration surface.
  External contributors (issue reporters, PR authors, external
  reviewers) work against this. Because it mirrors continuously
  from Dev, WIP is visible early — that's intentional. Manuel-tier
  research collaborators sit here.
- **Release at `emergi-foundation`** is the canonical citation
  target. Only tagged, quality-gated releases land here. The
  foundation already stewards adjacent energy work (`embit`,
  `emjoule`, `Footprint`, `Efficiency`, `reporting`, `EmergiPlan`,
  `DeepSolar`). Adding the `emburden*` package tree fits its scope
  and makes the citation story clean — "cite the foundation as
  publisher, cite the maintainer's ORCID as author".

## Adjacent orgs (not in the flow)

- `emrgi/` — personal energy-brand aggregation, mostly forks of
  external tooling (pvlib, rdtools, PyPSA, PYPOWER). Kept separate;
  not the emburden release target.
- `altfund/`, `ominari-insights/` — finance and prediction-markets
  lines respectively. Independent from the emburden ecosystem.

## Repo-to-tier map (as of 2026-09-19)

The 14 packages in the emburden ecosystem plus companion sites:

| Package | Dev | Mirror | Release target |
|:---|:---|:---|:---|
| `emburden` (net_energy_equity) | ScheierVentures | ericscheier | emergi-foundation |
| `emburdendata` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdengeo` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenstats` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenutil` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenweather` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdender` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenhealth` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenvis` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenpub` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdentest` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdenplus` | ScheierVentures | ericscheier | emergi-foundation |
| `emburdensynth` | ScheierVentures | ericscheier | emergi-foundation |
| `energese` | ScheierVentures | ericscheier | emergi-foundation |
| Site (`emburden-site`) | ericscheier | ericscheier | ericscheier |
| Staging (`emburden-site-staging`) | ericscheier | ericscheier | (auto) |

`emburden-site` is the exception — it's a companion site not a
package, and its deploy uses the ericscheier repo directly. Not
retargeting.

## Publication workflow (per release)

The path from a Dev commit to a Release tag:

1. **Dev branch**: work on ScheierVentures private mirror. Feature
   branches, WIP, exploratory scripts. Commit and push freely.
2. **Public sync to Mirror**: every push of `main` / `global` / `ssa`
   also pushes to `ericscheier/<repo>` via the `public` remote (see
   `git remote -v` — every ecosystem repo has both `scheier` and
   `public` remotes configured, so `git push all main` fans out).
3. **Pre-release scrub** (per repo, before tagging a release):
   - Confirm no named individuals in code, docstrings, or docs
     (per `CONTRIBUTING.md`'s naming policy). Grep with
     `git grep -inE '<known-collaborator-names>'` from a private
     wordlist.
   - Confirm no secrets in code or history. `git log -p | grep -iE
     'secret|token|api_key|password'`.
   - Confirm gated-data caches are gitignored (IEA WEB, DHS
     microdata, Afrobarometer merged rounds).
   - Confirm `AUTHORS.md`, `CITATION.cff`, `CONTRIBUTING.md`,
     `CODE_OF_CONDUCT.md`, `LICENSE` are current at repo root.
   - `devtools::check()` (or `R CMD check`) clean for R packages.
4. **Tag the release**: `git tag -a vX.Y.Z -m "release notes"`.
5. **Mirror to Release org**:
   - First time: create the repo on `emergi-foundation` with the
     same name.
   - Add a remote: `git remote add release git@github.com:emergi-foundation/<repo>.git`.
   - `git push release main --tags` on the tagged release.
   - Optional: enable GitHub Actions from Release; disable
     issues/PRs on Release and route to Mirror to keep one canonical
     issue tracker.
6. **Update citation targets**: the release commit + tag are what
   Zenodo, CRAN, and JOSS should reference. `CITATION.cff` should
   list `repository-code: https://github.com/emergi-foundation/<repo>`.
7. **Update the site**: `emburden-site` paper cards and package
   pages point at `emergi-foundation/<repo>` from the release
   forward.

## Ongoing publication cadence

- Dev → Mirror: continuous (every push).
- Mirror → Release: per tagged version. Suggested cadence: monthly
  for active packages during heavy development; quarterly or
  per-milestone once the API stabilises. Releases are rendezvous
  points — no in-between commits go to Release.

## Authorship in this workflow

- Commit `Author:` line stays with the maintainer identity
  (`eric@scheier.org`, transitioning to `info@emburden.org` via
  `.mailmap` once activated).
- `AUTHORS.md` at each repo lists the maintainer as "emburden
  project" (role-based) with the maintainer ORCID.
- `CITATION.cff` at each repo lists the same role-based author.
- Zenodo release DOIs, when minted, cite the foundation as
  publisher and the ORCID as author.
- No named individuals appear in released code or docs by default;
  external contributors opt into named credit via `AUTHORS.md`.

## Foundation onboarding TODOs (user-gated)

None of these are automatable from a code session; they're org-
admin tasks that need the user in the GitHub UI:

- [ ] Create `emergi-foundation/<pkg>` empty repo (per package, at
      first release).
- [ ] Set `AGPL-3.0-or-later` license from the GitHub template on
      each new repo (matches the source repo).
- [ ] Turn off issues + wiki on Release repos; keep them on Mirror.
      Add a README banner "issues live at
      github.com/ericscheier/<pkg>/issues".
- [ ] Optional: enable GitHub Pages on the Release repo for the
      pkgdown site if we want per-package sites hosted at
      `emergi-foundation.github.io/<pkg>/`. Currently pkgdown is
      served from `pkg.emburden.org` via the ericscheier repo — that
      can stay, or move to the foundation later.
- [ ] Zenodo integration: enable Zenodo → GitHub webhook on the
      Release org so tagged releases mint DOIs automatically.

## Change log

- 2026-09-19: initial version. Replaced a prior draft that assumed a
  destination `emburden/*` org migration; the correct destination is
  `emergi-foundation/*` per its role as the ecosystem's nonprofit
  steward.
