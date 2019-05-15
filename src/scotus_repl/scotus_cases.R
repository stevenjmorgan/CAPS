rm(list=ls())
setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")

library(quanteda)

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

comb$ari <- NA
comb$rix <- NA
comb$coleman_liau <- NA
comb$coleman_liau_short <- NA
comb$dan_bryan <- NA
comb$dick_stew <- NA
comb$elf <- NA
comb$farr <- NA
comb$flesh <- NA
comb$flesh_kin <- NA
comb$forcast <- NA
comb$fucks <- NA
comb$FOG <- NA
comb$linsear <- NA
comb$nws <- NA
comb$smog <- NA
comb$strain <- NA
comb$wheeler <- NA

comb$opin_text <- as.character(comb$opin_text)

#Encoding(comb$opin_text[1]) <- "UTF-8"
#iconv(comb$opin_text[1], "UTF-8", "UTF-8",sub='')

# Calculate readability
for (i in 1:nrow(comb)) {
  
  # Calculate scores on each doc.
  measures <- textstat_readability(comb$opin_text[i], measure = 'all')
  
  # Store each in dataframe
  comb$ari[i] <- measures$ARI
  comb$rix[i] <- measures$RIX
  comb$coleman_liau[i] <- measures$Coleman.Liau.grade
  comb$coleman_liau_short[i] <- measures$Coleman.Liau.grade
  comb$dan_bryan[i] <- measures$Danielson.Bryan
  comb$dick_stew[i] <- measures$Dickes.Steiwer
  comb$elf[i] <- measures$ELF
  comb$farr[i] <- measures$Farr.Jenkins.Paterson
  comb$flesh[i] <- measures$Flesch
  comb$flesh_kin[i] <- measures$Flesch.Kincaid
  comb$forcast[i] <- measures$FORCAST
  comb$fucks[i] <- measures$Fucks
  comb$FOG[i] <- measures$FOG
  comb$linsear[i] <- measures$Linsear.Write
  comb$nws[i] <- measures$nWS
  comb$smog[i] <- measures$SMOG
  comb$strain[i] <- measures$Strain
  comb$wheeler[i] <- measures$Wheeler.Smith
  
  # Print out progress every 250 iterations
  if(i %% 250==0){
    cat(paste0("Iteration: ", i, "\n"))
  }
}

### PCA