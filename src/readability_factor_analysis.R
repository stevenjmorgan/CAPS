# This script runs factor analysis & PCA on the 6 readability measures.

rm(list=ls())
#setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")
setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")

library(psych)
library(ggplot2)
library(stats)
library(reshape2)
library(lavaan)
library(MVN)
library(gtable)
library(gridExtra)
library(plyr)


#all_cases <- read.csv('state_court_cases_no_cites_50min.csv') #state_court_cases.csv
#all_cases <- read.csv('state_court_wide_final4-12.csv')
all_cases <- read.csv('state_court_wide_final4-23.csv')

all_cases <- all_cases[which(all_cases$year >= 1776),]
summary(all_cases$pos_cites)
all_cases$pos_cites[is.na(all_cases$pos_cites)] <- 0
all_cases$neg_cites[is.na(all_cases$neg_cites)] <- 0

#setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Min50")

# Subset data to only include readability measures
keep.vars <- c('ari','coleman_liau', 'flesch', 'flesch_kincaid', 'gunning_fog',
               'smog', 'number_cites', 'pos_cites', 'neg_cites')
allcases_read <- all_cases[, (names(all_cases) %in% keep.vars)]


# Plot distributions
p1 <- ggplot(allcases_read, aes(x=ari)) + geom_density() + xlim(c(0,100)) + xlab('ARI') + ylim(c(0,0.3))
p2 <- ggplot(allcases_read, aes(x=coleman_liau)) + geom_density() + xlim(c(0,100)) + xlab('Coleman-Liau') + ylim(c(0,0.3))
p3 <- ggplot(allcases_read, aes(x=flesch)) + geom_density() + xlim(c(0,100)) + xlab('Fleisch') + ylim(c(0,0.3))
p4 <- ggplot(allcases_read, aes(x=flesch_kincaid)) + geom_density() + xlim(c(0,100)) + xlab('Fleisch-Kincaid') + ylim(c(0,0.3))
p5 <- ggplot(allcases_read, aes(x=gunning_fog)) + geom_density() + xlim(c(0,100)) + xlab('Gunning-Fog') + ylim(c(0,0.3))
p6 <- ggplot(allcases_read, aes(x=smog)) + geom_density() + xlim(c(0,100)) + xlab('SMOG') + ylim(c(0,0.3))

png('density_plots_read.png')
grid.arrange(p1, p2, p3, p4, p5, p6, ncol=3)
dev.off()

summary(all_cases$smog)
hist(all_cases$smog)
summary(all_cases$smog < 5) # Count a number of sentences (at least 30)
summary(all_cases$smog == 0)

# Fit model
cfa.model <- 'f1 =~ ari + coleman_liau + 0*flesch + flesch_kincaid + gunning_fog + smog
              f2 =~ ari + coleman_liau + flesch + flesch_kincaid + 0*gunning_fog + smog'
cfa.fit <- cfa(cfa.model, data=allcases_read, std.lv=T, std.ov=T)
summary(cfa.fit)

# Observed covariance matrix (with denominator n)
#s1 <- cov(cfa.model) * (nrow(cfa.model)-1)/nrow(cfa.model)

parameterEstimates(cfa.fit)
inspect(cfa.fit,what="std")
inspect(cfa.fit,what="std")$lambda
inspect(cfa.fit,what = "std")$beta


# Maximum Likelihood Factor Analysis w/ promax rotation (measures should not be
# orthogonal)
fact.vars <- c('ari','coleman_liau', 'flesch', 'flesch_kincaid', 'gunning_fog','smog')
fit <- factanal(allcases_read[,(names(allcases_read) %in% fact.vars)], 3, rotation="promax")
print(fit, digits=2, cutoff=.3, sort=TRUE)
# plot factor 1 by factor 2 
load <- fit$loadings[,1:2] 
png('fa3_promax.png')
plot(load,type="n", main = 'Factor Loadings: 3FA w/ Promax Rotation') # set up plot 
text(load,labels=names(allcases_read),cex=.7)
dev.off()

# Maximum Likelihood Factor Analysis w/ promax rotation w/ 2 factors
# (measures should not be orthogonal)
fit.2f.pro <- factanal(allcases_read[,(names(allcases_read) %in% fact.vars)], 2, rotation="promax")
print(fit.2f.pro, digits=2, cutoff=.3, sort=TRUE)
# plot factor 1 by factor 2 
load <- fit.2f.pro$loadings[,1:2]
png('fa2_promax.png')
plot(load,type="n", main = 'Factor Loadings: 2FA w/ Promax Rotation') # set up plot 
text(load,labels=names(allcases_read),cex=.7) # add variable names
dev.off()

# Maximum Likelihood Factor Analysis w/ varimax rotation 
fit.var <- factanal(allcases_read[,(names(allcases_read) %in% fact.vars)], 3, rotation="varimax")
print(fit.var, digits=2, cutoff=.3, sort=TRUE)
# plot factor 1 by factor 2 
load <- fit.var$loadings[,1:2]
png('fa3_varimax.png')
plot(load,type="n", main = 'Factor Loadings: 3FA w/ Varimax Rotation') # set up plot 
text(load,labels=names(allcases_read),cex=.7) # add variable names
dev.off()

# Maximum Likelihood Factor Analysis w/ varimax rotation w/ 2 factors 
fit.var.2f <- factanal(allcases_read[,(names(allcases_read) %in% fact.vars)], 2, rotation="varimax")
print(fit.var.2f, digits=2, cutoff=.3, sort=TRUE)
# plot factor 1 by factor 2 
load <- fit.var.2f$loadings[,1:2]
png('fa2_varimax.png')
plot(load,type="n", main = 'Factor Loadings: 2FA w/ Varimax Rotation') # set up plot 
text(load,labels=names(allcases_read),cex=.7) # add variable names
dev.off()

# Extract first factor based on 2 factor varimax rotation
fit.final <- factanal(allcases_read[,(names(allcases_read) %in% fact.vars)], 2,
                scores=c("regression"),
                rotation="varimax")
print(fit.final, digits=2, cutoff=.3, sort=TRUE)
head(fit.final$scores)
factor_1_2 <- as.data.frame(fit.final$scores)
all_cases_factors <- cbind(all_cases, factor_1_2)

# PCA
pca.fit <- princomp(allcases_read[,(names(allcases_read) %in% fact.vars)], cor=TRUE)
summary(pca.fit)
png('scree_plot.png')
plot(pca.fit,type="lines", main = 'Scree Plot: Proportion of Variance Explained of Six Readability Measures')
dev.off()
#pca.fit$scores # the principal components
#biplot(pca.fit) # Runs for a WHILE
pca.scores <- as.data.frame(pca.fit$scores)

# PCA w/ varimax rotation
pca.rotated <- psych::principal(allcases_read[,(names(allcases_read) %in% fact.vars)], rotate="varimax", nfactors=3, scores=TRUE)
print(pca.rotated$scores[1:5,])


######## To be deleted -> done in python code
#x <- read.csv('state_temp.csv')
#head(x)
#all_cases_factors <- cbind(all_cases_factors, x$state)
#colnames(all_cases_factors)[16] <- 'state'
#############

# Convert state vector to character
all_cases_factors$state <- as.character(all_cases_factors$state)

# Combine pca scores (raw, not loadings)
all_cases_factors <- cbind(all_cases_factors, pca.scores)

#Combine pca varimax scores
all_cases_factors <- cbind(all_cases_factors, as.data.frame(pca.rotated$scores))
colnames(all_cases_factors)

# Group by decade, average 1st factor of readability scores
#state_dec_pairs <- as.data.frame(table(all_cases_factors$decade, all_cases_factors$state))
#colnames(state_dec_pairs) <- c('decade','state','freq')
#state_dec_pairs <- state_dec_pairs[which(state_dec_pairs$freq > 0),]
state_decade_1f <- aggregate(all_cases_factors[,c('Factor1','Factor2', "Comp.1",
                                                  "Comp.2", "RC1", "RC2", 'ari',
                                                  'coleman_liau', 'flesch',
                                                  'flesch_kincaid', 'smog',
                                                  'gunning_fog', 'word_count')], 
                                                  #'SCOTUS_cites', 'total_cites',
                                                  #us_cites')], 
                             list(all_cases_factors$state, all_cases_factors$decade), mean)
colnames(state_decade_1f) <- c('state','decade','average_1f','average_2f', 
                               'average_pc1','average_pc2', 'average_rc1',
                               'average_rc2', 'average_ari', 'average_coleman',
                               'average_flesch', 'average_fk', 'average_smog',
                               'average_gf','average_word_count')#, 'average_scotus',
                               #'average_total_cite', 'average_us_cites')
state_decade_1f <- state_decade_1f[with(state_decade_1f, order(state, decade)),]


decade_1f <- aggregate(all_cases_factors[,c('Factor1','Factor2', "Comp.1",
                                                  "Comp.2", "RC1", "RC2", 'ari',
                                                  'coleman_liau', 'flesch',
                                                  'flesch_kincaid', 'smog',
                                                  'gunning_fog', 'word_count')], 
                             #'SCOTUS_cites', 'total_cites',
                             #us_cites')], 
                             list(all_cases_factors$decade), mean)
year_1f <- aggregate(all_cases_factors[,c('Factor1','Factor2', "Comp.1",
                                          "Comp.2", "RC1", "RC2", 'ari',
                                          'coleman_liau', 'flesch',
                                          'flesch_kincaid', 'smog',
                                          'gunning_fog', 'word_count')], 
                     #'SCOTUS_cites', 'total_cites',
                     #us_cites')], 
                     list(all_cases_factors$year), mean)

# Group by year-state median, sort by state
year_state_1f <- aggregate(all_cases_factors[,c('Factor1','Factor2', "Comp.1",
                                          "Comp.2", "RC1", "RC2", 'ari',
                                          'coleman_liau', 'flesch',
                                          'flesch_kincaid', 'smog',
                                          'gunning_fog', 'word_count',
                                          'number_cites', 'pos_cites', 
                                          'neg_cites')], 
                     #'SCOTUS_cites', 'total_cites',
                     #us_cites')], 
                     list(all_cases_factors$state, all_cases_factors$year), median)
colnames(year_state_1f)[1] <- 'state'
colnames(year_state_1f)[2] <- 'year'
freq <- count(all_cases_factors, vars=c("year","state"))
year_state_1f <- merge(year_state_1f, freq, by = c('state','year'), all.x = TRUE)
year_state_1f <- year_state_1f[order(year_state_1f$state, year_state_1f$year),]
View(year_state_1f)

save(year_state_1f, file = 'year_state_measures.RData')


### Plot average factor score by decade by state
states <- as.character(unique(state_decade_1f$state))
pdf('average_1f_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average First Factor Readability Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_1f)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average First Factor: Readability") +
    #xlim(1740, 2020) +
  theme_bw()
  print(final.plot)
}
dev.off() 

pdf('average_2f_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Second Factor Readability Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_2f)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average Second Factor: Readability") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 


# Plot 1f scores by decade





# Plot average PC scores by decade by state
pdf('average_pc1_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average First Principal Component Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_pc1)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average First Principal Component Score: Readability") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 

pdf('average_pc2_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Second Principal Component Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_pc2)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average Second Principal Component Score: Readability") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 

# Plot average rotated PC scores by decade by state
pdf('average_rc1_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Varimax-Rotated First Principal Component Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_rc1)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average Varimax-Rotated First Principal Component Score: Readability") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 

pdf('average_rc2_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Varimax-Rotated Second Principal Component Score:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_rc2)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average Varimax-Rotated Second Principal Component Score: Readability") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 


## Plot readability scores separately by decade
pdf('average_all_scores_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Readability Scores:",states[i], 'High Court')
  final.plot <- ggplot(state_decade_1f[which(state_decade_1f$state == states[i]),], aes(decade)) + 
    geom_line(aes(y = average_ari, colour = 'average_ari')) + 
    geom_line(aes(y = average_coleman, colour = 'average_coleman')) + 
    geom_line(aes(y = average_flesch, colour = 'average_flesch')) + 
    geom_line(aes(y = average_fk, colour = 'average_flesch_kincaid')) + 
    geom_line(aes(y = average_smog, colour = 'average_smog')) + 
    geom_line(aes(y = average_gf, colour = 'average_gunning_fog')) +
  labs(title=title,
       x="Decade", y = "Average Readability Scores") +
    theme_bw()
  print(final.plot)
}
dev.off() 

## Plot average word count separately by decade
pdf('average_wc_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of Words in Majority Opinion:",states[i], 'High Court')
  final.plot <- ggplot(state_decade_1f[which(state_decade_1f$state == states[i]),], aes(decade)) + 
    geom_line(aes(y = average_word_count)) +
    labs(title=title,
         x="Decade", y = "Average Word Count") +
    theme_bw()
  print(final.plot)
}
dev.off() 

### Calculate and plot readability scores by year
read.by.year <- aggregate(all_cases_factors[,c('ari', 'coleman_liau', 'flesch',
                                               'flesch_kincaid', 'smog',
                                               'gunning_fog', 'word_count',
                                               'SCOTUS_cites')],#, 'us_cites',
                                               #'total_cites')], 
                             list(all_cases_factors$state, all_cases_factors$year), mean)
colnames(read.by.year) <- c('state','year', 'average_ari', 'average_coleman',
                               'average_flesch', 'average_fk', 'average_smog',
                               'average_gf', 'average_wc')#, 'average_scotus',
                            #'average_us', 'average_total_cites')
read.by.year <- read.by.year[with(read.by.year, order(state, year)),]
pdf('average_read_year.pdf')
for (i in 1:length(states)) {
  title <- paste("Average Readability Scores:",states[i], 'High Court')
  final.plot <- ggplot(read.by.year[which(read.by.year$state == states[i]),], aes(year)) + 
    geom_line(aes(y = average_ari, colour = 'average_ari')) + 
    geom_line(aes(y = average_coleman, colour = 'average_coleman')) + 
    geom_line(aes(y = average_flesch, colour = 'average_flesch')) + 
    geom_line(aes(y = average_fk, colour = 'average_flesch_kincaid')) + 
    geom_line(aes(y = average_smog, colour = 'average_smog')) + 
    geom_line(aes(y = average_gf, colour = 'average_gunning_fog')) +
    labs(title=title,
         x="Year", y = "Average Readability Scores") +
    theme_bw()
  print(final.plot)
}
dev.off()

# Average word count binned by year
pdf('average_wc_year.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of Words in Majority Opinion:",states[i], 'High Court')
  final.plot <- ggplot(read.by.year[which(read.by.year$state == states[i]),], aes(year)) + 
    geom_line(aes(y = average_wc)) + 
    labs(title=title,
         x="Year", y = "Average Word Count") +
    theme_bw()
  print(final.plot)
}
dev.off()



##############################
# Citations
##############################

pdf('average_scotus_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of SCOTUS Cites:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_scotus)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average # of SCOTUS Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 

pdf('average_us_cites_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of US Federal Cites:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_us_cites)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average # of US Federal Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off() 

pdf('average_total_cites_decade.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of Total Cites:",states[i], 'High Court')
  final.plot <- ggplot(data=state_decade_1f[which(state_decade_1f$state == states[i]),], aes(x=decade, y=average_total_cite)) +
    geom_point(stat="identity") +
    labs(title=title,
         x="Decade", y = "Average # of Total Citations") +
    #xlim(1740, 2020) +
    theme_bw()
  print(final.plot)
}
dev.off()


pdf('average_total_cites_year.pdf')
for (i in 1:length(states)) {
  title <- paste("Average # of Total Cites:",states[i], 'High Court')
  final.plot <- ggplot(read.by.year[which(read.by.year$state == states[i]),], aes(year)) + 
    geom_line(aes(y = average_total_cites)) + 
    labs(title=title,
         x="Year", y = "Average Total Citesf") +
    theme_bw()
  print(final.plot)
}
dev.off()



all_cases$cites.test <- NA
all_cases$total.cites.test <- all_cases$SCOTUS_cites + all_cases$us_cites
for (i in 1:nrow(all_cases)) {
  if (all_cases$total.cites.test[i] == all_cases$total_cites[i]) {
    all_cases$cites.test[i] <- TRUE
  }
  else{
    all_cases$cites.test[i] <- FALSE
  }
  
}


