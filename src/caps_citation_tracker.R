### This script compares our citation measure w/ CAPS citation measure.

rm(list=ls())
setwd('C:/Users/SF515-51T/Desktop/CAPS')

load('firstdim.RData')
colnames(all.courts)
unique(all.courts$number_cites)

cites <- read.csv('citations.csv/citations.csv', header = F)
head(cites)

### Clean up adjancy file -> v1 should be one plus the value above
colnames(cites) <- c('source_case', 'v2', 'v3', 'v4', 'v5','v6','v7','v8',
                     'v9','v10','v11','v12','v13','v14')
cites$total.cites <- 0
cites$delete <- "keep"

#smp.cites <- cites[1:200,]
smp.cites <- cites
smp.cites$total.cites <- rowSums(!is.na(smp.cites))-3

rm(cites)

gc()

for (i in 2:nrow(smp.cites)) {

  if (i%%1000==0) {
    print(paste(i,'cases done!'))
  }
    
  if (smp.cites$delete[i-1] != 'DELETE' & (smp.cites$source_case[i] > (smp.cites$source_case[i-1] + 500) | smp.cites$source_case[i] < (smp.cites$source_case[i-1] - 500))) {
    smp.cites$total.cites[i-1] <- smp.cites$total.cites[i-1] + rowSums(!is.na(smp.cites))[i] - 2
    smp.cites$delete[i] <- 'DELETE'
    
    if (smp.cites$delete[i] == 'DELETE' & rowSums(!is.na(smp.cites))[i] == 16 & (smp.cites$source_case[i+1] > (smp.cites$source_case[i-1] + 500) | smp.cites$source_case[i+1] < (smp.cites$source_case[i-1] - 500))) {
      smp.cites$delete[i+1] <- 'DELETE' 
      ### ADD CITATION COUNT
      smp.cites$total.cites[i-1] <- smp.cites$total.cites[i-1] + rowSums(!is.na(smp.cites))[i+1] - 2
    }
    
    if (smp.cites$delete[i+1] == 'DELETE' & rowSums(!is.na(smp.cites))[i+1] == 16 & (smp.cites$source_case[i+2] >= (smp.cites$source_case[i-1] + 500) | smp.cites$source_case[i+2] <= (smp.cites$source_case[i-1] - 500))) {
      smp.cites$delete[i+2] <- 'DELETE' 
      smp.cites$total.cites[i-1] <- smp.cites$total.cites[i-1] + rowSums(!is.na(smp.cites))[i+2] - 2
      
    }
    
    if (smp.cites$delete[i+2] == 'DELETE' & rowSums(!is.na(smp.cites))[i+2] == 16 & (smp.cites$source_case[i+2] > (smp.cites$source_case[i-1] + 500) | smp.cites$source_case[i+3] < (smp.cites$source_case[i-1] - 500))) {
      smp.cites$delete[i+3] <- 'DELETE' 
      smp.cites$total.cites[i-1] <- smp.cites$total.cites[i-1] + rowSums(!is.na(smp.cites))[i+3] - 2
    }
    if (smp.cites$delete[i+3] == 'DELETE' & rowSums(!is.na(smp.cites))[i+3] == 16 & (smp.cites$source_case[i+3] > (smp.cites$source_case[i-1] + 500) | smp.cites$source_case[i+4] < (smp.cites$source_case[i-1] - 500))) {
      smp.cites$delete[i+4] <- 'DELETE' 
      smp.cites$total.cites[i-1] <- smp.cites$total.cites[i-1] + rowSums(!is.na(smp.cites))[i+4] - 2
    }
  }
  
}
