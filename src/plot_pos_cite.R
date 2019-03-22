# This script plots positive and negative citations by state over time.

rm(list=ls())
#setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")
setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")

library(ggplot2)
library(reshape2)
library(readstata13)
library(gridExtra)

cite <- read.csv('state_court_pos_cites.csv')
colnames(cite)
cite$cite <- as.character(cite$cite)

x <- cite[which(cite$state == 'Maryland'),]
dim(x)

# Read in stata file on judicial selection
j.sel <- read.dta13('judSelHist.dta')
write.csv(j.sel, file = 'selection.csv')

# Determine switches in judicial selection procedures
switch.ind <- numeric()
for (i in 2:nrow(j.sel)) {
  if (j.sel$method[i] != j.sel$method[i-1] && j.sel$stateabbr[i] == j.sel$stateabbr[i-1]
      && j.sel$method[i-1] != 'NA') {
    switch.ind <- c(switch.ind, i)
  }
}
print(switch.ind)
j.sel$stateabbr[538]; j.sel$year[538]


# AL 1867-1868, legislative election -> partisan election



### Calculate and plot readability scores by year
read.by.year <- aggregate(cite[,c('pos_cites', 'neg_cites', 'total_cites',
                                  'us_cites', 'SCOTUS_cites')], 
                          list(cite$state, cite$year), mean)
colnames(read.by.year) <- c('state','year', 'pos_cites', 'neg_cites', 
                            'total_cites', 'us_cites', 'SCOTUS_cites')
read.by.year <- read.by.year[with(read.by.year, order(state, year)),]

### Plot # of citations by year by state
states <- as.character(unique(read.by.year$state))
pdf('average_citations_year.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Number of Citations:",states[i], 'High Court')
  final.plot <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=total_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 


################
pdf('average_citations_year.pdf')
final.plot <- list()
for (i in 1:length(states)) {
  title <- paste("Average Number of Citations:
          ",states[i], 'High Court')
  final.plot[[i]] <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=total_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  #print(final.plot)
}
do.call(grid.arrange, final.plot[1:6])
do.call(grid.arrange, final.plot[7:12])
do.call(grid.arrange, final.plot[13:18])
do.call(grid.arrange, final.plot[19:24])
do.call(grid.arrange, final.plot[25:30])
do.call(grid.arrange, final.plot[31:36])
do.call(grid.arrange, final.plot[37:42])
do.call(grid.arrange, final.plot[43:48])
do.call(grid.arrange, final.plot[49:50])
#grid.arrange(final.plot)
dev.off()

################

### Plot # of SCOTUS reporter citations by year by state
pdf('average_scotus_citations_year.pdf')
final.plot <- list()
for (i in 1:length(states)) {
  title <- paste("Average Number of SCOTUS Citations:",states[i], 'High Court')
  final.plot[[i]] <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=SCOTUS_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # SCOTUS Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  #print(final.plot)
}
do.call(grid.arrange, final.plot[1:6])
do.call(grid.arrange, final.plot[7:12])
do.call(grid.arrange, final.plot[13:18])
do.call(grid.arrange, final.plot[19:24])
do.call(grid.arrange, final.plot[25:30])
do.call(grid.arrange, final.plot[31:36])
do.call(grid.arrange, final.plot[37:42])
do.call(grid.arrange, final.plot[43:48])
do.call(grid.arrange, final.plot[49:50])
dev.off()

### Plot # of federal reporter citations by year by state
pdf('average_fed_citations_year.pdf')
final.plot <- list()
for (i in 1:length(states)) {
  title <- paste("Average Number of Federal Reporter Citations:",states[i], 'High Court')
  final.plot[[i]] <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=us_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # Federal Reporter Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  #print(final.plot)
}
do.call(grid.arrange, final.plot[1:6])
do.call(grid.arrange, final.plot[7:12])
do.call(grid.arrange, final.plot[13:18])
do.call(grid.arrange, final.plot[19:24])
do.call(grid.arrange, final.plot[25:30])
do.call(grid.arrange, final.plot[31:36])
do.call(grid.arrange, final.plot[37:42])
do.call(grid.arrange, final.plot[43:48])
do.call(grid.arrange, final.plot[49:50])
dev.off()

### Plot # of positive citations by year by state
pdf('average_pos_citations_year.pdf')
final.plot <- list()
for (i in 1:length(states)) {
  title <- paste("Average Number of Positive Citations:",states[i], 'High Court')
  final.plot[[i]] <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=pos_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # Positive Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  #print(final.plot)
}
do.call(grid.arrange, final.plot[1:6])
do.call(grid.arrange, final.plot[7:12])
do.call(grid.arrange, final.plot[13:18])
do.call(grid.arrange, final.plot[19:24])
do.call(grid.arrange, final.plot[25:30])
do.call(grid.arrange, final.plot[31:36])
do.call(grid.arrange, final.plot[37:42])
do.call(grid.arrange, final.plot[43:48])
do.call(grid.arrange, final.plot[49:50])
dev.off() 

### Plot # of negative citations by year by state
pdf('average_neg_citations_year.pdf')
final.plot <- list()
for (i in 1:length(states)) {
  title <- paste("Average Number of Negative Citations:",states[i], 'High Court')
  final.plot[[i]] <- ggplot(data=read.by.year[which(read.by.year$state == states[i]),], aes(x=year, y=neg_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Year", y = "Average # Negative Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  #print(final.plot)
}
do.call(grid.arrange, final.plot[1:6])
do.call(grid.arrange, final.plot[7:12])
do.call(grid.arrange, final.plot[13:18])
do.call(grid.arrange, final.plot[19:24])
do.call(grid.arrange, final.plot[25:30])
do.call(grid.arrange, final.plot[31:36])
do.call(grid.arrange, final.plot[37:42])
do.call(grid.arrange, final.plot[43:48])
do.call(grid.arrange, final.plot[49:50])
dev.off() 


### Sample cases for validation
library(dplyr)

set.seed(24519)
sample <- sample_n(cite, 100)
sample_cases <- as.data.frame(cbind(as.character(sample$cite), sample$total_cites))
colnames(sample_cases) <- c('case', 'total_cites')

write.csv(sample_cases, file = 'validate_cites_2-27.csv', row.names = FALSE)
