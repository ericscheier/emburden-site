# Private-to-public transition plan for the emburden ecosystem

This is the ecosystem-wide plan for moving 14+ repos from personal
`ericscheier/*` hosting to `emburden` organisation hosting, and for
managing repos that have been developed privately with AI-assisted
tooling before public release. It applies to any current or future
`emburden`-branded repo.

## Current state

- **Hosting**: 14 public repos under `github.com/ericscheier/*` (main
  package tree: `emburden`, `emburdendata`, `emburdengeo`,
  `emburdenstats`, `emburdenutil`, `emburdenweather`, `emburdender`,
  `emburdenhealth`, `emburdenvis`, `emburdenpub`, `emburdentest`,
  `emburdenplus`, `emburdensynth`, `energese`, plus companion sites
  `emburden-site`, `emburden-site-staging`).
- **Mirror**: private mirror of most repos under
  `github.com/ScheierVentures/*` for backup and access-control
  flexibility.
- **License**: AGPL-3.0-or-later across the ecosystem.
- **Contact**: `info@emburden.org`.
- **Author identity in commits**: Eric Scheier (`eric@scheier.org`).
  Move to `info@emburden.org` is planned but not yet executed - see
  §3 below.
- **AI-collaboration**: previously tagged in commit messages via
  `Co-Authored-By: Claude ...` and `Claude-Session: ...` lines
  (~310 commits across the ecosystem). Going forward, project policy
  omits these lines (see §4). The `AUTHORS.md` at each repo carries
  the project-level AI-collaboration disclosure.

## 1. Org migration

The intent is to move all `ericscheier/emburden*` repos to an
`emburden` GitHub organisation once the org is registered. Sequence:

1. **Register the `emburden` GitHub org** with `info@emburden.org` as
   the billing / notification contact.
2. **Transfer each repo** via GitHub Settings → Danger Zone →
   Transfer ownership. GitHub redirects old URLs
   (`github.com/ericscheier/foo` → `github.com/emburden/foo`) for
   ~1 year post-transfer with no config on our side, and `git clone`
   of the old URL keeps working over that window.
3. **Update pkgdown / CRAN references**:
   - `_pkgdown.yml`: `url: https://pkg.emburden.org` (already set).
   - Each package's `DESCRIPTION`: `URL` and `BugReports` fields
     point at `github.com/emburden/<pkg>`.
   - `CITATION.cff`: `repository-code` field.
   - README badges (CI, coverage, CRAN status) — regenerate for the
     new URL.
4. **Update the paper**: `docs/paper/global_emergy_alpha.Rmd` and
   `manuscript/*` cite `github.com/ericscheier/*` repos; global-replace
   to `github.com/emburden/*` after org transfer.
5. **Update `emburden-site` links**: `papers.Rmd`, README badges,
   any `href` references.
6. **CI secrets**: transfer or re-add tokens on the new org (GitHub
   does *not* migrate Actions secrets on org transfer).

**Do not** rename the branches, tags, or the git history on transfer.
GitHub keeps them intact and the redirect handles the URL move.
Forcing a rewrite of history would be destructive and disrupt any
downstream clone.

## 2. Private-to-public repo release (individual repos)

For repos that live private for a period before public release (e.g.
in-development manuscript branches, sensitive data explorers), the
recommended release sequence is:

1. **Scrub named individuals** from documentation, comments, and code
   using the pattern in `emburdensynth/docs/q3_47_scrub/` (search
   for maintainer names, collaborator names, personal email addresses;
   replace with role-based labels — "project maintainer", "external
   reviewer", "external collaborator" — per the naming policy in each
   repo's `CONTRIBUTING.md`).
2. **Confirm the license file** is `AGPL-3.0-or-later` and matches the
   ecosystem baseline.
3. **Add** `CONTRIBUTING.md`, `AUTHORS.md`, `CITATION.cff`,
   `CODE_OF_CONDUCT.md`. Template these from `emburdensynth/`.
4. **Confirm gated data sources** (IEA WEB, DHS microdata,
   Afrobarometer / Latinobarómetro merged rounds, LEAP, etc.) are
   gitignored and covered by an env-var-based access gate (see
   `emburdendata` for the pattern: `IEA_LICENCE_ACKNOWLEDGED=true`).
   Every gated source is listed in the repo's README with its
   licence status.
5. **Squash internal-planning docs** that don't belong in public
   history. Move to a private notes location; add the file pattern
   to `.gitignore` so the same shape does not slip back in.
6. **Sanity-scan `git log`** for surprising commit messages, embedded
   tokens, or accidental large binaries. `git log -p | grep -iE
   "secret|token|api_key|password"` catches most.
7. **Flip visibility** via GitHub Settings → Danger Zone → Change
   visibility to Public.

## 3. Author email transition

Current commits: `Author: ericscheier <eric@scheier.org>`.
Target: `Author: ericscheier <info@emburden.org>`.

Do **not** rewrite historical author metadata - that is destructive
history rewriting and disrupts downstream clones. Instead:

- Set the git author email locally to `info@emburden.org` for future
  commits: `git config --local user.email info@emburden.org` (or
  `--global` if that's the intent across all machines).
- Optionally add a `.mailmap` at repo root that maps the historical
  `eric@scheier.org` commits to the canonical `info@emburden.org`
  identity for display purposes in `git log`, `git shortlog`, and
  GitHub's contributor list. `.mailmap` does not rewrite history; it
  aliases display.
- Sample `.mailmap` entry:
  ```
  emburden project <info@emburden.org> <eric@scheier.org>
  ```

## 4. AI-collaboration attribution policy

- **Commits going forward** do not append `Co-Authored-By: Claude ...`
  or `Claude-Session: ...` lines. This matches the project's
  naming-scrubbing policy for public output.
- **Historical commits** (~310 across the ecosystem) retain those
  lines. Retroactively stripping them would require force-pushing
  history to both remotes and would disrupt any downstream clone
  (in particular an external collaborator who is already tracking
  `emburdensynth/ssa`). The judgement recorded on 2026-09-19 is
  that commit-log metadata visible only via `git log` is not worth
  the disruption; the project-level AI-collaboration disclosure at
  `AUTHORS.md` is the canonical statement.
- **Paper text** and **site content** do not name AI collaborators,
  the maintainer, or external collaborators in the rendered output.
  `AUTHORS.md` carries the disclosure separately.

## 5. Contributor-name policy

Named individual attribution is opt-in. See §3 of each repo's
`CONTRIBUTING.md`. `git log` remains the raw record; `AUTHORS.md` is
the aggregated view. Contributors who prefer role-based attribution
default to unnamed listing under the appropriate role.

## Timeline

Order of operations, roughly:

1. Org registration + transfer (this doc's §1) — user-gated, no code
   changes needed on our side.
2. Author email transition (§3) — one `git config` change per repo,
   `.mailmap` files added at repo root, no history rewrite.
3. Paper / site link updates (§1 step 4-5) — mechanical global-replace
   once the transfer lands.
4. `.gitignore` + naming-scrub audit on each repo before any
   remaining private-to-public flip (§2).

This document is the single source of truth for the ecosystem
transition. Individual repo `CONTRIBUTING.md` files reference it.
