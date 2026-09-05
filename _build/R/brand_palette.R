# =============================================================================
# emburden + emrgi brand palette wrapper for the analytic report
# -----------------------------------------------------------------------------
# Consolidates the emburden-org publication palette (from `emburdenpub`,
# Color-Universal-Design compliant) and the emrgi.com portal brand colors
# (from emrgi/static/portal.css) so every chart in the analytic report can
# reach for a canonical set. The two palettes are complementary:
#
#   emburdenpub sequential/diverging/categorical — the science-grade CUD
#       palettes for burden gradients, temporal change, and discrete groups.
#
#   emrgi brand (g/gd/gdd/gold/charge/ink/mut/bg/line) — the web-app brand
#       used for framing (title/subtitle text colour, positive-accent
#       primary green, gold highlight, charge-red for warning/burden peaks,
#       ink for body text, bg for plot background).
#
# theme_emburden_emrgi() sets the ggplot theme to match the portal CSS
# (Montserrat/HelveticaNeue text stack, forest-green accents, off-white bg).
# =============================================================================

#' emrgi portal brand colors as a named vector
#'
#' Source of truth: emrgi/emrgi/static/portal.css `:root { --g:#228b22; ... }`.
#' Kept in sync manually — if portal.css changes, update here.
#' @export
emrgi_brand_colors <- function() {
  c(
    g       = "#228b22",   # primary forest green
    gd      = "#176b17",   # dark green (hover/active)
    gdd     = "#0f4d0f",   # darkest green
    gold    = "#b5791b",   # gold accent
    ink     = "#1d2a1d",   # body text
    mut     = "#566656",   # muted/subtitle text
    line    = "#d6e4d6",   # dividers
    bg      = "#f3f8f3",   # off-white green background
    charge  = "#c0392b",   # danger/burden peak red
    warn    = "#8a5a16"    # warning brown
  )
}

#' Categorical scale drawing on emrgi brand + emburdenpub CUD
#'
#' Order: forest-green, gold, charge-red, warn-brown, then CUD categorical
#' colours 5-8 for extras. Good for up to 8 categories, colourblind-safe.
#' @export
emburden_emrgi_categorical <- function(n = 5) {
  br <- emrgi_brand_colors()
  # Base 5 emrgi anchors + 10 extra CUD-adjacent colors → up to 15
  # unique hues before falling back to grDevices::hcl.colors.
  cud_extra <- c("#7570b3","#e7298a","#66a61e","#a6761d","#666666",
                  "#1b9e77","#d95f02","#08519c","#ffbf00","#8b0000")
  colours <- c(br[["g"]], br[["gold"]], br[["charge"]], br[["gd"]],
                br[["mut"]], cud_extra)
  if (n <= length(colours)) return(colours[seq_len(n)])
  # Extend with hcl.colors keeping perceptual distance
  extra <- grDevices::hcl.colors(n - length(colours) + 2, palette = "Set 3")
  c(colours, extra[-c(1, length(extra))])[seq_len(n)]
}

#' Burden sequential — yellow -> emrgi-green -> blue (emburdenpub anchored)
#'
#' Uses `emburdenpub::get_burden_palette("sequential")` when available,
#' falls back to a hand-built 6-stop gradient that ends in emrgi-forest-green
#' + a darker cool-blue tail for the highest burden values.
#' @export
burden_sequential_colors <- function() {
  if (requireNamespace("emburdenpub", quietly = TRUE)) {
    return(emburdenpub::get_burden_palette("sequential"))
  }
  c("#ffffcc","#c7e9b4","#7fcdbb","#41b6c4","#2c7fb8","#253494")
}

#' Diverging — emrgi charge-red -> off-white -> emrgi-green (CUD-safe)
#'
#' For maps like "within-country burden inequality (Q1 − Q5, pp)". Uses
#' emrgi's charge-red and forest-green so it visually ties into the app.
#' @export
burden_diverging_colors <- function() {
  br <- emrgi_brand_colors()
  # Interpolate 9 stops
  c(br[["charge"]], "#e08072", "#f2b8ae", "#f8dbd4",
    br[["bg"]],
    "#d0e5c8", "#8fbf7e", "#4d9a3b", br[["gdd"]])
}

#' ggplot theme matching the emrgi portal CSS
#'
#' Off-white background, forest-green title text, muted-green subtitle,
#' ink body text, Montserrat family with system fallbacks.
#' @export
theme_emburden_emrgi <- function(base_size = 11) {
  br <- emrgi_brand_colors()
  # Portal.css sets Montserrat first; use it only if the system has it
  # installed, else fall back to the sans stack that R can guaranteed
  # render (avoids "invalid font type" crashes on headless systems).
  available_fonts <- tryCatch(systemfonts::system_fonts()$family,
                                error = function(e) character(0))
  fam <- if ("Montserrat" %in% available_fonts) "Montserrat" else "sans"
  # Tufte-adjacent: minimize non-data ink, bottom-legend default with a
  # single horizontal row, muted grid to draw the eye to the data.
  ggplot2::theme_minimal(base_size = base_size, base_family = fam) +
    ggplot2::theme(
      plot.background   = ggplot2::element_rect(fill = br[["bg"]], colour = NA),
      panel.background  = ggplot2::element_rect(fill = br[["bg"]], colour = NA),
      panel.grid.major  = ggplot2::element_line(colour = ggplot2::alpha(br[["line"]], 0.7),
                                                 linewidth = 0.25),
      panel.grid.minor  = ggplot2::element_blank(),   # cut minor grid noise
      plot.title        = ggplot2::element_text(face = "bold",
                                                 colour = br[["gd"]],
                                                 size = base_size * 1.25,
                                                 margin = ggplot2::margin(b = 4)),
      plot.subtitle     = ggplot2::element_text(colour = br[["mut"]],
                                                 size = base_size * 0.9,
                                                 margin = ggplot2::margin(b = 8)),
      plot.caption      = ggplot2::element_text(colour = br[["mut"]],
                                                 size = base_size * 0.75,
                                                 hjust = 0,
                                                 margin = ggplot2::margin(t = 6)),
      axis.text         = ggplot2::element_text(colour = br[["ink"]],
                                                 size = base_size * 0.85),
      axis.title        = ggplot2::element_text(colour = br[["ink"]],
                                                 size = base_size * 0.9),
      axis.ticks        = ggplot2::element_line(colour = ggplot2::alpha(br[["mut"]], 0.5),
                                                 linewidth = 0.25),
      legend.position   = "bottom",
      legend.direction  = "horizontal",
      legend.background = ggplot2::element_rect(fill = br[["bg"]], colour = NA),
      legend.key        = ggplot2::element_rect(fill = br[["bg"]], colour = NA),
      legend.margin     = ggplot2::margin(t = 4, b = 0, l = 0, r = 0),
      legend.box.margin = ggplot2::margin(t = 2, b = 2, l = 0, r = 0),
      legend.title      = ggplot2::element_text(colour = br[["gd"]], face = "bold",
                                                 size = base_size * 0.85),
      legend.text       = ggplot2::element_text(colour = br[["ink"]],
                                                 size = base_size * 0.8),
      strip.text        = ggplot2::element_text(colour = br[["gd"]], face = "bold",
                                                 size = base_size * 0.9),
      strip.background  = ggplot2::element_rect(fill = ggplot2::alpha(br[["line"]], 0.3),
                                                 colour = NA),
      plot.title.position = "plot",
      plot.caption.position = "plot")
}
