rm(list=ls())
setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")

library(quanteda)

cases <- read.csv('state_court_text.csv')

cases$ari <- NA
cases$rix <- NA
cases$coleman_liau <- NA
cases$coleman_liau_short <- NA
cases$dan_bryan <- NA
cases$dick_stew <- NA
cases$elf <- NA
cases$farr <- NA
cases$flesh <- NA
cases$flesh_kin <- NA
cases$forcast <- NA
cases$fucks <- NA
cases$FOG <- NA
cases$linsear <- NA
cases$nws <- NA
cases$smog <- NA
cases$strain <- NA
cases$wheeler <- NA

cases$opin_text <- as.character(cases$opin_text)

# Calculate readability
for (i in 1:nrow(cases)) {
  
  # Calculate scores on each doc.
  measures <- textstat_readability(cases$text[i], measure = 'all')
  
  # Store each in dataframe
  cases$ari[i] <- measures$ARI
  cases$rix[i] <- measures$RIX
  cases$coleman_liau[i] <- measures$Coleman.Liau.grade
  cases$coleman_liau_short[i] <- measures$Coleman.Liau.grade
  cases$dan_bryan[i] <- measures$Danielson.Bryan
  cases$dick_stew[i] <- measures$Dickes.Steiwer
  cases$elf[i] <- measures$ELF
  cases$farr[i] <- measures$Farr.Jenkins.Paterson
  cases$flesh[i] <- measures$Flesch
  cases$flesh_kin[i] <- measures$Flesch.Kincaid
  cases$forcast[i] <- measures$FORCAST
  cases$fucks[i] <- measures$Fucks
  cases$FOG[i] <- measures$FOG
  cases$linsear[i] <- measures$Linsear.Write
  cases$nws[i] <- measures$nWS
  cases$smog[i] <- measures$SMOG
  cases$strain[i] <- measures$Strain
  cases$wheeler[i] <- measures$Wheeler.Smith
  
  # Print out progress every 250 iterations
  if(i %% 10000==0){
    cat(paste0("Iteration: ", i, "\n"))
  }
}

cases <- cases[,-c('text')]