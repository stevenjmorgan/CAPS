### This script conducts PCA on SCOTUS readability measure and compares to
### the BYU lingustics corpus and State Supreme Court readability measures

rm(list=ls())
setwd('C:/Users/SF515-51T/Desktop/CAPS')

library(factoextra)
library(ggplot2)
library(dplyr)
library(plyr)

scotus <- read.csv('benchmark_SCOTUS_readability.csv')
colnames(scotus)
length(unique(scotus$cite))

# De-duplicate SCOTUS cases
scotus <- scotus[!duplicated(scotus$cite),]

# Count cases by year, plot
