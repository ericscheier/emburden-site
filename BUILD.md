# Build + deploy

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
