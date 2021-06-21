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

read_dataframe <- function(type, file_name) {
    type <- match.arg(type,
              c(
                  "XLSX",
                  "CSV",
                  "TSV"
              ))
    if (type == "XLSX") {
        return(openxlsx::read.xlsx(xlsxFile = file_name))
    } else if (type == "CSV") {
        return(read.csv(xlsxFile = file_name))
    } else if (type == "TSV") {
        return(read.delim(xlsxFile = file_name))
    }
}

library(openxlsx)

study_data_file_type <- match.arg(study_data_file_type,
                                  c(
                                      "XLSX",
                                      "CSV",
                                      "TSV"
                                  ))

meta_data_file_type <- match.arg(meta_data_file_type,
                                  c(
                                      "XLSX",
                                      "CSV",
                                      "TSV"
                                  ))

message(sprintf("Reading %s...", dQuote(study_data_file)))
study_data <- read_dataframe(study_data_file_type,
                             study_data_file)
message(sprintf("Reading %s...", dQuote(meta_data_file)))
meta_data <- read_dataframe(meta_data_file_type,
                            meta_data_file)

library(dataquieR)
library(parallel)

sd0 <- study_data
md0 <- meta_data

checks <- NULL
code_labels <- NULL

if (length(splitargs$checks) > 0 &&
    length(splitargs$checks_file_type) > 0) {
    splitargs$checks_file_type <- match.arg(splitargs$checks_file_type,
                                     c(
                                         "XLSX",
                                         "CSV",
                                         "TSV"
                                     ))
    message(sprintf("Reading %s...", dQuote(splitargs$checks)))
    checks <- read_dataframe(splitargs$checks_file_type,
                             splitargs$checks)
}

if (length(splitargs$code_labels) > 0 &&
    length(splitargs$code_labels_file_type) > 0) {
    splitargs$code_labels_file_type <- 
        match.arg(splitargs$code_labels_file_type,
                                            c(
                                                "XLSX",
                                                "CSV",
                                                "TSV"
                                            ))
    message(sprintf("Reading %s...", dQuote(splitargs$code_labels)))
    code_labels <- read_dataframe(splitargs$code_labels_file_type,
                             splitargs$code_labels)
}

r <- dq_report(study_data = sd0, meta_data = md0, cores = 
                   parallelly::availableCores(),
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
