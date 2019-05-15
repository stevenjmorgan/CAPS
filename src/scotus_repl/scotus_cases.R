rm(list=ls())
setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")


# Read in data from SCOTUS database
load('SCDB_2018_02_caseCentered_Citation.Rdata')

SCDB_2018_02_caseCentered_Citation$year <- as.numeric(substring(SCDB_2018_02_caseCentered_Citation$dateDecision, 1, 4))
scotus <- SCDB_2018_02_caseCentered_Citation[which(SCDB_2018_02_caseCentered_Citation$year >= 1953 & 
                                                   SCDB_2018_02_caseCentered_Citation$year <= 2007 &
                                                   SCDB_2018_02_caseCentered_Citation$decisionType == 1),]
#-1*(5574-7317) ### 1743

summary(scotus$decisionType == 1)


# Old data
#load('SCDB_2012_01_caseCentered_Citation.Rdata')
#SCDB_2012_01_caseCentered_Citation$year <- as.numeric(substring(SCDB_2012_01_caseCentered_Citation$dateDecision, 1, 4))
#scotus1 <- SCDB_2012_01_caseCentered_Citation[which(SCDB_2012_01_caseCentered_Citation$year >= 1953 & 
#                                                   SCDB_2012_01_caseCentered_Citation$year <= 2007 &
#                                                   SCDB_2012_01_caseCentered_Citation$decisionType == 1),]


# Read in SCOTUS CAP data
scotus_cap <- read.csv('scotus_rep.csv')
colnames(scotus_cap)
scotus_cap$cite <- as.character(scotus_cap$cite)
scotus_cap <- scotus_cap[,c('cite','opin_text')]

# Merge in text data
comb <- merge(scotus, scotus_cap, by.x = 'usCite', by.y = 'cite', all.x = F)
write.csv(comb, 'scotus_subset.csv')
