# This script reads in the data on non-majority opinions, 
# produces visualizations, and compare readability scores.

rm(list=ls())
setwd('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP')
#setwd('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP')

library(tidyverse)
library(ggplot2)

# Read in non-maj opin data
non_major <- read.csv('nonmajority_opins.csv')

# Group by year and decade
non_major$state <- as.character(non_major$state)
year.group <- plyr::count(non_major, 'year')
dec.group <- plyr::count(non_major, 'decade')

# Plot non-majority opinions
g <- ggplot(data = year.group, aes(x = year, y = freq)) + 
  geom_point() + labs(x = 'Year', y = '# Non-Majority Opinions')
g
ggsave('non_maj_opins_year.png')

g1 <- ggplot(data = dec.group, aes(x = decade, y = freq)) + 
  geom_point() + labs(x = 'Decade', y = '# Non-Majority Opinions')
g1
ggsave('non_maj_opins_dec.png')


# Dissenting opinions by year and decade
year.group.dissent <- plyr::count(non_major[which(non_major$opin_type == 'dissent'),], 'year')
dec.group.dissent <- plyr::count(non_major[which(non_major$opin_type == 'dissent'),], 'decade')

# Plot dissents
g2 <- ggplot(data = year.group.dissent, aes(x = year, y = freq)) + 
  geom_point() + labs(x = 'Year', y = '# Dissenting Opinions')
g2
ggsave('dissents_year.png')

g3 <- ggplot(data = dec.group.dissent, aes(x = decade, y = freq)) + 
  geom_point() + labs(x = 'Decade', y = '# Dissenting Opinions')
g3
ggsave('dissents_dec.png')


# Proportion of cases with dissenting opinion - year
year.prop.dissent <- merge(year.group, year.group.dissent, by = 'year',
                           all.x = TRUE, all.y = TRUE)
year.prop.dissent$freq.y[is.na(year.prop.dissent$freq.y)] <- 0
colnames(year.prop.dissent)[2] <- 'Total.Opinions'
colnames(year.prop.dissent)[3] <- 'Dissents'
year.prop.dissent$dissent.prop <- year.prop.dissent$Dissents/year.prop.dissent$Total.Opinions

# Plot proportion of cases with dissent - year
ggplot(data = year.prop.dissent, aes(x = year, y = dissent.prop)) + 
  geom_point() + labs(x = 'Year', y = 'Prop. of Cases w/ Dissenting Opinions')
ggsave('prop_dissents_year.png')

# Proportion of cases with dissenting opinion - decade
dec.prop.dissent <- merge(dec.group, dec.group.dissent, by = 'decade',
                           all.x = TRUE, all.y = TRUE)
dec.prop.dissent$freq.y[is.na(dec.prop.dissent$freq.y)] <- 0
colnames(dec.prop.dissent)[2] <- 'Total.Opinions'
colnames(dec.prop.dissent)[3] <- 'Dissents'
dec.prop.dissent$dissent.prop <- dec.prop.dissent$Dissents/dec.prop.dissent$Total.Opinions

# Plot proportion of cases with dissent - decade
ggplot(data = dec.prop.dissent, aes(x = decade, y = dissent.prop)) + 
  geom_point() + labs(x = 'Decade', y = 'Prop. of Cases w/ Dissenting Opinions')
ggsave('prop_dissents_dec.png')


# Concurring opinions by year and decade
year.group.concur <- plyr::count(non_major[which(non_major$opin_type == 'concurrence'),], 'year')
dec.group.concur <- plyr::count(non_major[which(non_major$opin_type == 'concurrence'),], 'decade')

# Plot concurrences
g4 <- ggplot(data = year.group.concur, aes(x = year, y = freq)) + 
  geom_point() + labs(x = 'Year', y = '# Concurring Opinions')
g4
ggsave('concur_year.png')

g5 <- ggplot(data = dec.group.concur, aes(x = decade, y = freq)) + 
  geom_point() + labs(x = 'Decade', y = '# Concurring Opinions')
g5
ggsave('concur_dec.png')


# Proportion of cases with concurring opinion - year
year.prop.concur <- merge(year.group, year.group.concur, by = 'year',
                           all.x = TRUE, all.y = TRUE)
year.prop.concur$freq.y[is.na(year.prop.concur$freq.y)] <- 0
colnames(year.prop.concur)[2] <- 'Total.Opinions'
colnames(year.prop.concur)[3] <- 'Concurrences'
year.prop.concur$concur.prop <- year.prop.concur$Concurrences/year.prop.concur$Total.Opinions

# Plot proportion of cases with dissent - year
ggplot(data = year.prop.concur, aes(x = year, y = concur.prop)) + 
  geom_point() + labs(x = 'Year', y = 'Prop. of Cases w/ Concurring Opinions')
ggsave('prop_concur_year.png')

# Proportion of cases with dissenting opinion - decade
dec.prop.concur <- merge(dec.group, dec.group.concur, by = 'decade',
                          all.x = TRUE, all.y = TRUE)
dec.prop.concur$freq.y[is.na(dec.prop.concur$freq.y)] <- 0
colnames(dec.prop.concur)[2] <- 'Total.Opinions'
colnames(dec.prop.concur)[3] <- 'Concurrences'
dec.prop.concur$concur.prop <- dec.prop.concur$Concurrences/dec.prop.concur$Total.Opinions

# Plot proportion of cases with dissent - decade
ggplot(data = dec.prop.concur, aes(x = decade, y = concur.prop)) + 
  geom_point() + labs(x = 'Decade', y = 'Prop. of Cases w/ Concurring Opinions')
ggsave('prop_concur_dec.png')



#### Readability Measures
# Calculate average by year for each measure
year.scores <- aggregate(non_major[,c('ari','coleman_liau','flesch',
                                      'flesch_kincaid','smog','gunning_fog',
                                      'word_count','number_cites')], 
                           list(non_major$year), mean)
colnames(year.scores)[1] <- 'year'

# Plot average individual scores by year
ggplot(year.scores, aes(year)) + 
  geom_line(aes(y = ari, colour = 'ari')) + 
  geom_line(aes(y = coleman_liau, colour = 'coleman')) + 
  geom_line(aes(y = flesch, colour = 'flesch')) + 
  geom_line(aes(y = flesch_kincaid, colour = 'flesch_kincaid')) + 
  geom_line(aes(y = smog, colour = 'smog')) + 
  geom_line(aes(y = gunning_fog, colour = 'gunning_fog')) +
  labs(x='Year', y = 'Average Readability Scores') +
  theme_bw()
ggsave('read.year.png')

# Calculate average by decade for each measure
dec.scores <- aggregate(non_major[,c('ari','coleman_liau','flesch',
                                      'flesch_kincaid','smog','gunning_fog',
                                      'word_count','number_cites')], 
                         list(non_major$decade), mean)
colnames(dec.scores)[1] <- 'decade'

# Plot average individual scores by year
ggplot(dec.scores, aes(decade)) + 
  geom_line(aes(y = ari, colour = 'ari')) + 
  geom_line(aes(y = coleman_liau, colour = 'coleman')) + 
  geom_line(aes(y = flesch, colour = 'flesch')) + 
  geom_line(aes(y = flesch_kincaid, colour = 'flesch_kincaid')) + 
  geom_line(aes(y = smog, colour = 'smog')) + 
  geom_line(aes(y = gunning_fog, colour = 'gunning_fog')) +
  labs(x='Decade', y = 'Average Readability Scores') +
  theme_bw()
ggsave('read.decade.png')



##### Citations
# Plot average number of citations per case by year
ggplot(data = year.scores, aes(x = year, y = number_cites)) + 
  geom_point() + labs(x = 'Year', y = 'Average # Citations')
ggsave('non_maj_citations.png')

# Plot average number of citations per case by decade
ggplot(data = dec.scores, aes(x = decade, y = number_cites)) + 
  geom_point() + labs(x = 'Decade', y = 'Average # Citations')
ggsave('non_maj_citations_dec.png')


# Citations in dissenting opinions
dissents <- non_major[which(non_major$opin_type=='dissent'),]
year.scores.dis <- aggregate(dissents[,c('ari','coleman_liau','flesch',
                                      'flesch_kincaid','smog','gunning_fog',
                                      'word_count','number_cites')], 
                         list(dissents$year), mean)
colnames(year.scores.dis)[1] <- 'year'

ggplot(data = year.scores.dis, aes(x = year, y = number_cites)) + 
  geom_point() + labs(x = 'Year', y = 'Average # Citations')
ggsave('dissent_citations_yr.png')

dec.scores.dis <- aggregate(dissents[,c('ari','coleman_liau','flesch',
                                         'flesch_kincaid','smog','gunning_fog',
                                         'word_count','number_cites')], 
                             list(dissents$decade), mean)
colnames(dec.scores.dis)[1] <- 'decade'

ggplot(data = dec.scores.dis, aes(x = decade, y = number_cites)) + 
  geom_point() + labs(x = 'Decade', y = 'Average # Citations')
ggsave('dissent_citations_dec.png')


# Citations in concurring opinions
concurs <- non_major[which(non_major$opin_type=='concurrence'),]
year.scores.concur <- aggregate(concurs[,c('ari','coleman_liau','flesch',
                                         'flesch_kincaid','smog','gunning_fog',
                                         'word_count','number_cites')], 
                             list(concurs$year), mean)
colnames(year.scores.concur)[1] <- 'year'

ggplot(data = year.scores.concur, aes(x = year, y = number_cites)) + 
  geom_point() + labs(x = 'Year', y = 'Average # Citations')
ggsave('concur_citations_yr.png')

dec.scores.concur <- aggregate(concurs[,c('ari','coleman_liau','flesch',
                                           'flesch_kincaid','smog','gunning_fog',
                                           'word_count','number_cites')], 
                                list(concurs$decade), mean)
colnames(dec.scores.concur)[1] <- 'decade'

ggplot(data = dec.scores.concur, aes(x = decade, y = number_cites)) + 
  geom_point() + labs(x = 'Decade', y = 'Average # Citations')
ggsave('concur_citations_dec.png')


### Word counts
# All non-maj opinions
ggplot(data = year.scores, aes(x = year, y = word_count)) + 
  geom_point() + labs(x = 'Year', y = 'Average # of Words')
ggsave('word_count_yr.png')

ggplot(data = dec.scores, aes(x = decade, y = word_count)) + 
  geom_point() + labs(x = 'Decade', y = 'Average # of Words')
ggsave('word_count_dec.png')

# Dissenting opinions
ggplot(data = year.scores.dis, aes(x = year, y = word_count)) + 
  geom_point() + labs(x = 'Year', y = 'Average # of Words')
ggsave('dissent_word_count_yr.png')

# Concurring opinions
ggplot(data = year.scores.concur, aes(x = year, y = word_count)) + 
  geom_point() + labs(x = 'Year', y = 'Average # of Words')
ggsave('concur_word_count_yr.png')
