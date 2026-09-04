# emburden.org — ecosystem site

Public site for the [emburden R ecosystem](https://github.com/ericscheier).
Hosts the atlas, methods, data provenance, papers-in-flight, and code
overview. The per-package pkgdown reference docs live separately at
[ericscheier.github.io/emburden](https://ericscheier.github.io/emburden/)
(auto-built from the `emburden` R package repo).

## Environments

See [`ENVIRONMENTS.md`](ENVIRONMENTS.md) for the full dev → staging → prod
flow. In short:

- `dev` branch → local only, no deployment
- `staging` branch → https://staging.emburden.org
- `master` branch → https://emburden.org

Mirrors the pattern used by `ericscheier/ericscheier.github.io`.

## Content

- `index.Rmd` — landing page with the 67× climate-justice headline
- `atlas.Rmd` — global burden atlas, embedded ggplot figures
- `methods.Rmd` — five-phase pipeline + NEB math
- `data.Rmd` — data provenance table (17 sources 1750-2025)
- `papers.Rmd` — Science / Joule / Nature Energy / JSS / JOSS in flight
- `code.Rmd` — ecosystem overview + install snippets
- `styles/emburden.css` — emrgi/emburden brand palette

## Build stack

R Markdown (`rmarkdown::render_site()`) with `bslib`-themed
`flatly`-based Bootstrap 5, Montserrat + Inter + JetBrains Mono fonts.
Renders to `_build/`.

## License

MIT. Content: CC-BY 4.0 with attribution to Emrgi + Eric Scheier.
