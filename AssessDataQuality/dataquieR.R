#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

study_data_file <- args[[1]]
study_data_file_type <- args[[2]]

meta_data_file <- args[[3]]
meta_data_file_type <- args[[4]]

label_col <- args[[5]]

add_args <- tail(args, -5)

if (length(add_args)) {
    splitargs <- strsplit(add_args, "\\s*=\\s*", perl = TRUE)
    if (!all(vapply(splitargs, length, FUN.VALUE = integer(1)) == 2)) {
        stop(paste("Cannot parse command line arguments: ", deparse(add_args)))
    }
    splitargs <- do.call(rbind.data.frame, splitargs)
    colnames(splitargs) <- c("k", "v")
    splitargs <- as.list(setNames(splitargs$v, nm = splitargs$k))
}

library(openxlsx)
if (study_data_file_type != "XLSX") {
    stop("Cannot handle other file types than Excel yet.")
}
if (meta_data_file_type != "XLSX") {
    stop("Cannot handle other file types than Excel yet.")
}

message(sprintf("Reading %s...", dQuote(study_data_file)))
study_data <- openxlsx::read.xlsx(xlsxFile = study_data_file)
message(sprintf("Reading %s...", dQuote(meta_data_file)))
meta_data <- openxlsx::read.xlsx(xlsxFile = meta_data_file)

library(dataquieR)
library(parallel)

#load(system.file("extdata", "study_data.RData", package = "dataquieR"))
#load(system.file("extdata", "meta_data.RData", package = "dataquieR"))
#code_labels <- read.csv2(system.file("extdata",
#                                     "Missing-Codes-2020.csv",
#                                     package = "dataquieR"),
#                         stringsAsFactors = FALSE, na.strings = c())
#checks <- read.csv(system.file("extdata",
#                               "contradiction_checks.csv",
#                               package = "dataquieR"),
#                   header = TRUE, sep = "#")
sd0 <- study_data
md0 <- meta_data

checks <- NULL
code_labels <- NULL

if (length(splitargs$checks) > 0) {
    # checks <-
}

if (length(splitargs$code_labels) > 0) {
    # code_labels <-
}

# sd0 <- readRDS(system.file("extdata", "ship.RDS", package = "dataquieR"))
# md0 <- readRDS(system.file("extdata", "ship_meta.RDS", package = "dataquieR"))

r <- dq_report(study_data = sd0, meta_data = md0, cores = detectCores() - 1, # use maybe parallelly::availableCores() instead?
               dimensions = c("Completeness", "Consistency", "Accuracy"),
               label_col = label_col,
               check_table     = checks,
               cause_label_df  = code_labels,
               include_sysmiss = TRUE
)

o <- options(viewer = function(f) {})
on.exit(options(o))
fn <- print(r)
file.copy(fn, "report.html")
