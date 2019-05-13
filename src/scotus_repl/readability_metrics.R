install.packages('quanteda')
library(quanteda)

setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")

scotus <- read.csv('scotus_rep.csv')
scotus$opin_text <- as.character(scotus$opin_text)

x <- scotus$opin_text[1]
x

tagged.text <- treetag(x, treetagger="manual", lang="en", TT.options=list(path="~/bin/treetagger/", preset="en"))
hyph.txt.en <- hyphen(x, hyph.pattern = 'en')


scotus.metrics <- textstat_readability('These chickens tastte really good. Iw want more.', measure = 'Coleman.Liau.Grade')
y <- textstat_readability('These chickens tastte really good. Iw want more.', measure = 'Coleman.Liau.grade')

.libPaths()
