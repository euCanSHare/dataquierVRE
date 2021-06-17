#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

p <- args[[1]]
v <- args[[2]]

if (!requireNamespace(p, quietly=TRUE) || 
    compareVersion(v, as.character(packageVersion(p))) > 0) {

   stop(paste0('Need ', p, '(>=', v, ')'))

}
