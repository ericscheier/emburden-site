# Dynamic-count helpers for emburden.org site pages.
# Every .Rmd's setup chunk can `source("R/counts.R")` and use these
# instead of hardcoding numbers.

#' Number of unique ISO3 codes in a cached RDS
#' @param rds Filename in `docs/global_analysis_data/`, e.g. "cell_grid_wide.rds"
#' @param col Column name holding ISO3 codes (default "iso3")
#' @param data_dir Cache directory (default resolves to emburdensynth's cache)
iso3_count <- function(rds, col = "iso3", data_dir = NULL) {
  if (is.null(data_dir)) data_dir <- .resolve_data_dir()
  p <- file.path(data_dir, rds)
  if (!file.exists(p)) return(NA_integer_)
  d <- readRDS(p)
  # Handle list-of-df returns (some caches wrap multiple frames)
  if (is.list(d) && !is.data.frame(d)) {
    hit <- Filter(function(x) is.data.frame(x) && col %in% names(x), d)
    if (length(hit) == 0L) return(NA_integer_)
    d <- hit[[1]]
  }
  if (!col %in% names(d)) return(NA_integer_)
  length(unique(d[[col]]))
}

#' Row count of a cached RDS (or of a named sub-frame if the file is a list)
n_rows <- function(rds, sub = NULL, data_dir = NULL) {
  if (is.null(data_dir)) data_dir <- .resolve_data_dir()
  p <- file.path(data_dir, rds)
  if (!file.exists(p)) return(NA_integer_)
  d <- readRDS(p)
  if (!is.null(sub) && is.list(d) && !is.data.frame(d)) d <- d[[sub]]
  if (is.data.frame(d)) return(nrow(d))
  if (is.list(d)) return(length(d))
  length(d)
}

#' Year range from a cached RDS, formatted "min–max"
year_range <- function(rds, col = "year", sub = NULL, data_dir = NULL) {
  if (is.null(data_dir)) data_dir <- .resolve_data_dir()
  p <- file.path(data_dir, rds)
  if (!file.exists(p)) return("?–?")
  d <- readRDS(p)
  if (!is.null(sub) && is.list(d) && !is.data.frame(d)) d <- d[[sub]]
  if (is.list(d) && !is.data.frame(d)) {
    hit <- Filter(function(x) is.data.frame(x) && col %in% names(x), d)
    if (length(hit) == 0L) return("?–?")
    d <- hit[[1]]
  }
  if (!col %in% names(d)) return("?–?")
  rng <- range(d[[col]], na.rm = TRUE)
  sprintf("%d–%d", as.integer(rng[1]), as.integer(rng[2]))
}

#' Canonical burden coverage (live count of countries with a burden estimate)
canonical_burden_countries <- function(data_dir = NULL) {
  if (is.null(data_dir)) data_dir <- .resolve_data_dir()
  p <- file.path(data_dir, "summary_enriched.rds")
  if (!file.exists(p)) return(NA_integer_)
  s <- readRDS(p)
  sum(!is.na(s$burden_canonical))
}

#' Number of country parquets present on disk
cell_country_count <- function(pq_dir = NULL) {
  if (is.null(pq_dir)) pq_dir <- .resolve_pq_dir()
  if (!dir.exists(pq_dir)) return(NA_integer_)
  length(list.files(pq_dir, pattern = "_synthetic\\.parquet$"))
}

.resolve_data_dir <- function() {
  candidates <- c(
    "../docs/global_analysis_data",
    "../../emburdensynth/docs/global_analysis_data",
    file.path(Sys.getenv("HOME"),
              "Documents/apps/emburdensynth/docs/global_analysis_data")
  )
  hit <- candidates[dir.exists(candidates)][1]
  if (is.na(hit)) return(candidates[1])
  hit
}
.resolve_pq_dir <- function() {
  candidates <- c(
    "../output/global",
    "../../emburdensynth/output/global",
    file.path(Sys.getenv("HOME"),
              "Documents/apps/emburdensynth/output/global")
  )
  hit <- candidates[dir.exists(candidates)][1]
  if (is.na(hit)) return(candidates[1])
  hit
}
