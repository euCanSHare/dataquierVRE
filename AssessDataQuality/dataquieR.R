#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

study_data_file <- args[[1]]
study_data_file_type <- args[[2]]

meta_data_file <- args[[3]]
meta_data_file_type <- args[[4]]

label_col <- args[[5]]

add_args <- tail(args, -5)

if (length(add_args)) {
    splitargs <- strsplit(add_args, "\\s*=\\s*", perl = TRUE) # TODO only the first =
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

sd0 <- study_data
md0 <- meta_data

checks <- NULL
code_labels <- NULL

if (length(splitargs$checks) > 0 &&
    length(splitargs$checks_file_type) > 0) {
    if (splitargs$checks_file_type != "XLSX") {
        stop("Cannot handle other file types than Excel yet.")
    }
    message(sprintf("Reading %s...", dQuote(splitargs$checks)))
    checks <- openxlsx::read.xlsx(xlsxFile = splitargs$checks)
}

if (length(splitargs$code_labels) > 0 &&
    length(splitargs$code_labels_file_type) > 0) {
    if (splitargs$code_labels_file_type != "XLSX") {
        stop("Cannot handle other file types than Excel yet.")
    }
    message(sprintf("Reading %s...", dQuote(splitargs$code_labels)))
    code_labels <- openxlsx::read.xlsx(xlsxFile = splitargs$code_labels)
}

r <- dq_report(study_data = sd0, meta_data = md0, cores = parallelly::availableCores(),
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
