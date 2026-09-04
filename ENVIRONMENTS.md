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

`emburden.org` is registered at **Namecheap** and uses Namecheap's DNS
(`dns1.registrar-servers.com` / `dns2.registrar-servers.com`), not
Cloudflare. Records are edited in **Namecheap → Domain List → Manage →
Advanced DNS**.

Current state (as of 2026-09-04):

- `emburden.org` (apex) → 4 GitHub Pages A records
  (`185.199.108.153` `.109.153` `.110.153` `.111.153`) — resolves the
  pkgdown site served from `ericscheier/emburden`'s `gh-pages` branch.
- `www.emburden.org` → `CNAME ericscheier.github.io.`
- `staging.emburden.org` → does not exist yet

**To bring staging up**, add one CNAME record in Namecheap Advanced DNS:

| Type   | Host      | Value                        | TTL       |
|--------|-----------|------------------------------|-----------|
| CNAME  | `staging` | `ericscheier.github.io.`     | Automatic |

Then in Pages settings on **ericscheier/emburden-site-staging**,
under Custom domain, enter `staging.emburden.org` and let GitHub
issue the ACME certificate (typically 30-60s).

**To flip production to this ecosystem site** (deliberate cutover
after staging looks good):

1. In `ericscheier/emburden` → Settings → Pages → Custom domain:
   remove `emburden.org` (releases the domain from that repo).
2. In `ericscheier/emburden-site` → Settings → Pages → Custom domain:
   add `emburden.org` (claims it here; GitHub re-issues ACME cert).
3. No DNS changes required — the apex A records already point at
   GitHub Pages IPs.
4. Optionally: relocate the emburden pkgdown site to
   `pkg.emburden.org` by adding one more CNAME to
   `ericscheier.github.io.` and reconfiguring `ericscheier/emburden`'s
   Pages custom domain to `pkg.emburden.org`. Update `_pkgdown.yml`
   `url:` accordingly.

## What's automated vs manual

Automated (via `gh` in this repo's setup):
- `STAGING_DEPLOY_KEY` secret installed on `emburden-site`
- Deploy key with write access installed on `emburden-site-staging`
- Pages enabled on both repos with the right source config

Manual (needs a human at the Namecheap panel and GitHub Pages UI):
- The staging CNAME record above
- Entering `staging.emburden.org` as the Custom Domain in
  `emburden-site-staging`'s Pages settings
- The prod cutover steps above, when you're ready to flip
- Cloudflare is **not** involved for emburden.org (contrast with
  ericscheier.info which does sit behind Cloudflare)

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
