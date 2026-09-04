# Environments

| Branch    | Renders at                         | Deployed by                            |
|-----------|------------------------------------|----------------------------------------|
| `dev`     | nothing (local only)               | `Rscript -e 'rmarkdown::render_site()'` |
| `staging` | https://staging.emburden.org       | `.github/workflows/deploy-staging.yml`  |
| `master`  | https://emburden.org               | `.github/workflows/deploy-prod.yml`     |

## Flow

```
dev  ──PR──▶  staging  ──PR──▶  master
              (review the        (live)
               rendered site)
```

Mirrors the design pattern established for `ericscheier/ericscheier.github.io`.
Work on `dev`. Open a PR into `staging` to see the change rendered at
staging.emburden.org. Open a PR from `staging` into `master` to go live.

`master` requires a pull request — direct pushes are rejected. Both PR
targets run the checks in `.github/workflows/pr-checks.yml`: the site
must build and internal links must resolve.

## Why staging lives in another repository

GitHub Pages serves one site per repository, so a second rendered
environment needs somewhere else to live. The built output is pushed
to `ericscheier/emburden-site-staging`, whose Pages site is the
staging render.

The push is authenticated with an ed25519 deploy key scoped to that
repository alone, stored as the `STAGING_DEPLOY_KEY` secret here.
No account-wide token is involved. To rotate it: generate a new
keypair, replace the deploy key on `emburden-site-staging`, and update
the secret.

Staging serves `robots.txt` with `Disallow: /` so it never competes
with the live site in search results.

## DNS

- **Production**: `emburden.org` → currently pointing to `ericscheier/emburden`'s
  `gh-pages` branch (pkgdown site for the emburden R package).
  To switch to this ecosystem-wide site: change the `emburden.org` A/CNAME
  records to point at `ericscheier.github.io/emburden-site/`, then remove
  the CNAME record from `ericscheier/emburden/gh-pages` and enable Pages
  on this repo pointing at the built output.
- **Staging**: `staging.emburden.org` as a `CNAME` to
  `ericscheier.github.io` in the Cloudflare zone for `emburden.org`,
  set **DNS-only (grey cloud)**. Same rationale as
  `staging.ericscheier.info`: keep it unproxied so ACME can issue the
  Pages certificate.

## Build stack

- **Content**: R Markdown (`.Rmd`) sources in the repo root.
- **Renderer**: `rmarkdown::render_site()` reads `_site.yml` (like
  Jekyll reads `_config.yml`) and outputs to `_build/`.
- **CSS + assets**: `styles/emburden.css` applies the emrgi/emburden
  brand palette. Custom fonts pulled from Google Fonts via
  `styles/head_extras.html`.
- **Figures**: generated at render time from cached RDS in
  `../emburdensynth/docs/global_analysis_data/`; the CI runners
  install R + the emburden R packages before building.

## Deployment mechanism

Both environments deploy through GitHub Actions. Follows the same
approach used by ericscheier.info (deploy-pages@v4 for prod; a
peaceiris/actions-gh-pages push for staging because Pages allows
only one publish target per repo).

## Local dev

```bash
# Install R + emburden packages (one-time)
Rscript -e 'remotes::install_github(c("ericscheier/emburden",
                                       "ericscheier/emburdendata",
                                       "ericscheier/emburdensynth"))'

# Preview locally
Rscript -e 'rmarkdown::render_site(); servr::httd("_build")'
# → http://localhost:4321
```
