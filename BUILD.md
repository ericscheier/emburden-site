# Build + deploy

## Identity (Q3.21)

`identity.yml` at repo root is the single source of truth for the
project's public-facing identity: maintainer name, email
(`info@emburden.org`), organisation, canonical URLs, brand colours,
and the ecosystem palette (`bg_hex: "#f3f8f3"` — the page background
used across the site AND the paper PDF for a unified canvas).

It is a verbatim copy of `emburdensynth/config.yml`; keep them in
sync (both files, not just one) when changing any identity or brand
value. When either changes, re-render the affected pages so the
changes propagate.

GitHub namespace remains `ericscheier/` until a permanent hosting
decision is made. When it moves (org transfer or hand-off), update
`github_owner` in both files and re-render everything.

## Site architecture (current — Q3.21b)

**One domain (emburden.org), served by the pkgdown site**
(`net_energy_equity/docs/` → gh-pages of `ericscheier/emburden`).
The pkgdown site landing (`index.html`) IS the R-package page;
`reference/`, `articles/`, `news/` sit under it. Config in
`net_energy_equity/_pkgdown.yml` (`url: https://emburden.org`),
CNAME in `net_energy_equity/docs/CNAME`.

**staging.emburden.org** serves `emburden-site` (this repo) via
`.github/workflows/deploy-staging.yml`. That's where the multi-page
ecosystem draft lives — Home / Emergy / Access + QoS / Atlas /
Methods / Data / Papers / Code. It is a rehearsal of the eventual
subdomain split, not a shipped surface.

### Deferred redesign: pkg.emburden.org subdomain (Q3.20 target)

The intent was to split so `emburden.org` = ecosystem site and
`pkg.emburden.org` = pkgdown. That change is reverted for now because
it requires GH-UI custom-domain reconfiguration on both repos, and
without that step `emburden.org` returns a 404. To complete it when
ready:

1. Add DNS `pkg.emburden.org CNAME ericscheier.github.io`.
2. GH Pages settings on `ericscheier/emburden`: custom domain →
   `pkg.emburden.org`.
3. GH Pages settings on `ericscheier/emburden-site`: custom domain →
   `emburden.org` + Enforce HTTPS.
4. Change `net_energy_equity/_pkgdown.yml` `url:` back to
   `https://pkg.emburden.org`, `docs/CNAME` to `pkg.emburden.org`.
5. Change `emburden-site/_site.yml` right-nav href back to
   `https://pkg.emburden.org`.
6. Push both repos.



## Local render

The site's R Markdown sources reference figures + data from the
`emburdensynth` R repo (parent directory). To render, either:

**Option A — symlink emburdensynth paths in** (recommended, matches the
prior local build):

```bash
cd ~/Documents/apps/emburden-site
ln -sfn ../emburdensynth/R _ln_R
ln -sfn ../emburdensynth/docs _ln_docs
# Adjust paths in .Rmd chunks:
sed -i 's|../docs/global_analysis_data|_ln_docs/global_analysis_data|g; s|../R/brand_palette.R|_ln_R/brand_palette.R|g' *.Rmd
Rscript -e 'rmarkdown::render_site()'
# Restore paths:
sed -i 's|_ln_docs/global_analysis_data|../docs/global_analysis_data|g; s|_ln_R/brand_palette.R|../R/brand_palette.R|g' *.Rmd
rm _ln_R _ln_docs
```

**Option B — checkout emburdensynth alongside**:

```bash
cd ~/Documents/apps
git clone git@github.com:ericscheier/emburdensynth.git  # or ScheierVentures/
cd emburden-site
Rscript -e 'rmarkdown::render_site()'   # picks up ../emburdensynth/*
```

## Deploy

Commit both the `.Rmd` sources and the rebuilt `_build/` output.
Push to the branch matching your target environment:

- `dev` — local only, no CI
- `staging` — auto-deploys to https://staging.emburden.org
- `master` — auto-deploys to https://emburden.org

CI just uploads the pre-built `_build/`; no R runs on the server.

## Why pre-render (vs build-in-CI)?

The alternative — installing R + all emburden ecosystem packages on
every CI run — was tried first and abandoned. Root causes:

1. The R packages are private (`ScheierVentures/`), needing GH tokens
2. The site's Rmds read cached data files (17k cells, GB-scale) that
   would need to be re-generated on every CI run
3. Every 5-minute CI build for a 5-second content edit is a bad tradeoff

Committing the pre-built HTML makes deploys instant, and content
authors run the render locally at their own cadence.
