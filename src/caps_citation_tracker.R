### This script compares our citation measure w/ CAPS citation measure.

rm(list=ls())
setwd('C:/Users/SF515-51T/Desktop/CAPS')

load('firstdim.RData')
colnames(all.courts)
unique(all.courts$number_cites)

cites <- read.csv('citations.csv/citations.csv')
head(cites)
