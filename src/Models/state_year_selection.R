# This script creates a df of state-year-measure, merges in selection method
# data, and models opinion quality.

rm(list=ls())
setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")
#setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")

library(readstata13)
library(datasets)
library(stargazer)

load('year_state_measures.RData')

# Read in selection method data
judSel <- read.dta13('judSelHist.dta')

# Remove NA's
judSel <- judSel[!is.na(judSel$apt),]

# Read in states dataset
states <- as.data.frame(cbind(state.abb, state.name))

# Merge in abbreviations
year_state_1f <- merge(year_state_1f, states, by.x = 'state', by.y = 'state.name',
              all.x = TRUE)
year_state_1f <- merge(year_state_1f, judSel, by.x = c('state.abb','year'), 
              by.y = c('stateabbr','year'), all.x = TRUE)


## Models: Individual readability measures
colnames(year_state_1f)
selection.formula <- paste('apt','re','pe','freq','as.factor(state)','as.factor(year)', sep = '+')
fit.ari <- lm(paste('ari',selection.formula, sep='~'),
              data = year_state_1f)
summary(fit.ari)

fit.coleman_liau <- lm(paste('coleman_liau',selection.formula, sep='~'),
                       data = year_state_1f)
summary(fit.coleman_liau)

fit.flesch <- lm(paste('flesch',selection.formula, sep='~'),
                data = year_state_1f)
summary(fit.flesch)

fit.flesch_kincaid <- lm(paste('flesch_kincaid',selection.formula, sep='~'),
                         data = year_state_1f)
summary(fit.flesch_kincaid)

fit.smog <- lm(paste('smog',selection.formula, sep='~'),
               data = year_state_1f)
summary(fit.smog)

fit.gunning_fog <- lm(paste('gunning_fog',selection.formula, sep='~'),
                      data = year_state_1f)
summary(fit.gunning_fog)

fit.word_count <- lm(paste('word_count',selection.formula, sep='~'),
                     data = year_state_1f)
summary(fit.word_count)

stargazer(fit.ari, fit.coleman_liau, fit.flesch, fit.flesch_kincaid,
          fit.smog, fit.gunning_fog, fit.word_count, omit=c('year','state'),
          dep.var.labels = c('ARI','Coleman-Liau','Fleish','Fleish-Kincaid',
                            'SMOG','Gunning-Fog','Word Count'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))


## Model first factor in each state-year
fit.1f <- lm(paste('Factor1',selection.formula, sep='~'),
              data = year_state_1f)
summary(fit.1f)
stargazer(fit.1f, omit=c('year','state'),
          dep.var.labels = c('Readability: First Factor'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))


## Model citations
fit.total.cites <- lm(paste('number_cites',selection.formula,sep='~'),
                      data = year_state_1f)
summary(fit.total.cites)

fit.pos.cites <- lm(paste('pos_cites',selection.formula,sep='~'),
                      data = year_state_1f)
summary(fit.pos.cites)

fit.neg.cites <- lm(paste('neg_cites',selection.formula,sep='~'),
                    data = year_state_1f)
summary(fit.neg.cites)

stargazer(fit.total.cites, fit.pos.cites, fit.neg.cites, 
          omit=c('year','state'),
          dep.var.labels = c('Total Citations', 'Positive Citations', 
                             'Negative Citations'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))

# Poisson regression models of citations
fit.total.cites.pois <- glm(paste('number_cites',selection.formula,sep='~'),
                        data = year_state_1f, family = poisson)
summary(fit.total.cites.pois)

fit.pos.cites.pois <- glm(paste('pos_cites',selection.formula,sep='~'),
                      data = year_state_1f, family = poisson)
summary(fit.pos.cites.pois)

fit.neg.cites.pois <- glm(paste('neg_cites',selection.formula,sep='~'),
                      data = year_state_1f, family = poisson)
summary(fit.neg.cites.pois)

stargazer(fit.total.cites.pois, fit.pos.cites.pois, fit.neg.cites.pois, 
          omit=c('year','state'),
          dep.var.labels = c('Total Citations', 'Positive Citations', 
                             'Negative Citations'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))

# Logistic regression citations: does opinion cite a case?
year_state_1f$cite.bi <- ifelse(year_state_1f$number_cites > 0, 1, 0)
year_state_1f$pos.cite.bi <- ifelse(year_state_1f$pos_cites > 0, 1, 0)
year_state_1f$neg_cite.bi <- ifelse(year_state_1f$neg_cites > 0, 1, 0)

fit.total.cites.bi <- glm(paste('cite.bi',selection.formula,sep='~'),
                          data = year_state_1f, family = 'binomial')
summary(fit.total.cites.bi)

fit.pos.cites.bi <- glm(paste('pos.cite.bi',selection.formula,sep='~'),
                          data = year_state_1f, family = 'binomial')
summary(fit.pos.cites.bi)

fit.neg.cites.bi <- glm(paste('neg_cite.bi',selection.formula,sep='~'),
                          data = year_state_1f, family = 'binomial')
summary(fit.neg.cites.bi)