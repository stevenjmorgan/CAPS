# This script creates a df of state-year-measure, merges in selection method
# data, and models opinion quality.

rm(list=ls())
#setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")
#setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")
setwd('C:/Users/steve/Desktop/APSA_Paper')

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
year_state1d <- merge(year_state1d, states, by.x = 'state', by.y = 'state.name',
              all.x = TRUE)
year_state1d <- merge(year_state1d, judSel, by.x = c('state.abb','year'), 
              by.y = c('stateabbr','year'), all.x = TRUE)


## Models: Median first dimension
colnames(year_state1d)
selection.formula <- paste('apt','re','pe','freq','as.factor(state)','as.factor(year)', sep = '+')

fit.1d <- lm(paste('x',selection.formula, sep='~'),
              data = year_state1d)
summary(fit.1d)

stargazer(fit.1d, single.row = TRUE)


library(dotwhisker)
library(broom)
library(dplyr)

m1_df <- tidy(fit.1d)  %>% 
  filter(!grepl('as.fact*', term)) %>% 
  filter(term != "(Intercept)") %>% 
  filter(term != "freq")
dwplot(m1_df,dot_args = list(size = 3.5, pch = 21, fill = "white", col = 'black'),
       vline = geom_vline(xintercept = 0, colour = "grey60", linetype = 2),
       whisker_args = list(size = 3.5, col = 'red')) %>%
  relabel_predictors(c(apt = "Appointment",
                       re = "Retention Election",          
                       pe = "Partisan Election")) + #,
                       #freq = "Caseload")) 
    xlab("Coefficient Estimate") +
  theme_bw() +
  theme(text = element_text(size=25))
ggsave('reg1_results.png')


# Recode partisan and nonpartsian elections versus retention and appointed selection methods
year_state1d$re.appointed <- ifelse(year_state1d$re == 1 | year_state1d$apt == 1, 1, 0)
year_state1d$pe.np <- ifelse(year_state1d$pe == 1 | year_state1d$np == 1, 1, 0)

fit.1d.part.nonpart <- lm(x~pe.np+freq+as.factor(state)+as.factor(year),
              data = year_state1d)
summary(fit.1d.part.nonpart)

m2_df <- tidy(fit.1d.part.nonpart)  %>% 
  filter(!grepl('as.fact*', term)) %>% 
  filter(term != "(Intercept)")
dwplot(m2_df, vline = geom_vline(xintercept = 0, colour = "grey60", linetype = 2)) %>%
  relabel_predictors(c(pe.np = "Partisan or Non-Partisan Elections",
                       freq = "Caseload")) + xlab("Coefficient Estimate")
ggsave('reg2_results.png')



################################################################################
### Correlates of State policy merge ###
################################################################################
uri <- "http://ippsr.msu.edu/sites/default/files/correlatesofstatepolicyprojectv2_1.csv"
csp <- read.csv(uri)

summary(csp$leg_cont) #1= Democrats Control Both Chambers; 0= Democrats Control Neither Chamber; .5= Democrats Control One Chamber, .25= Demcorats Split Control of One Chamber, .75= Democrats Control One Chamber and Split Control of the Other
# 1937-2011
summary(csp$democrat) #Democratic Identifiers, 1956-2010 An over time measure of the percent of Democratic identifiers in each state
summary(csp$general_expenditure) #General State Expenditures, 1942 - 2016 General State Expenditures. All state government finance data are in $1,000s of current dollars.

# Merge in correlates data
csp <- csp[,c('st','year','leg_cont','democrat','general_expenditure')]
dim(year_state1d)
year_state1d <- merge(year_state1d, csp, by.x = c('state.abb', 'year'), 
           by.y = c('st','year'), all.x = TRUE)
dim(year_state1d)

# All selection methods
state.leg.fit <- lm(x~apt+re+pe+freq+leg_cont+general_expenditure + as.factor(year) + as.factor(state),
                    data = year_state1d)
summary(state.leg.fit)
stargazer(state.leg.fit)

m3_df <- tidy(state.leg.fit)  %>% 
  filter(!grepl('as.fact*', term)) %>% 
  filter(term != "(Intercept)")
dwplot(m3_df, dot_args = list(size = 3.5, pch = 21, fill = "white", col = 'black'), 
       vline = geom_vline(xintercept = 0, colour = "grey60", linetype = 2), whisker_args = list(size = 3.5, col = 'red')) %>%
  relabel_predictors(c(apt = "Appointment",
                       re = "Retention Election",          
                       pe = "Partisan Election",
                       freq = "Caseload",
                       leg_cont = 'Dem. Leg.',
                       general_expenditure = 'Gen. Expend.')) + xlab("Coefficient Estimate") +
  theme_bw() +
  theme(text = element_text(size=25))
ggsave('reg3_results.png')


# Partisan and non-partisan vs. other
state.leg.fit2 <- lm(x~pe.np+freq+leg_cont+general_expenditure + as.factor(year) + as.factor(state),
                    data = year_state1d)
summary(state.leg.fit2)

m4_df <- tidy(state.leg.fit2)  %>% 
  filter(!grepl('as.fact*', term)) %>% 
  filter(term != "(Intercept)")
dwplot(m4_df, vline = geom_vline(xintercept = 0, colour = "grey60", linetype = 2)) %>%
  relabel_predictors(c(pe.np = "Partisan or Non-Partisan Elections",
                       freq = "Caseload",
                       leg_cont = 'Dem. Leg.',
                       general_expenditure = 'Gen. Expend.')) + xlab("Coefficient Estimate")
ggsave('reg4_results.png')




################################################################################


# Individual readability measures
fit.ari <- lm(paste('ari',selection.formula, sep='~'),
              data = year_state1d)
summary(fit.ari)

fit.coleman_liau <- lm(paste('coleman_liau',selection.formula, sep='~'),
                       data = year_state1d)
summary(fit.coleman_liau)

fit.flesch <- lm(paste('flesch',selection.formula, sep='~'),
                data = year_state1d)
summary(fit.flesch)

fit.flesch_kincaid <- lm(paste('flesch_kincaid',selection.formula, sep='~'),
                         data = year_state1d)
summary(fit.flesch_kincaid)

fit.smog <- lm(paste('smog',selection.formula, sep='~'),
               data = year_state1d)
summary(fit.smog)

fit.gunning_fog <- lm(paste('gunning_fog',selection.formula, sep='~'),
                      data = year_state1d)
summary(fit.gunning_fog)

fit.word_count <- lm(paste('word_count',selection.formula, sep='~'),
                     data = year_state1d)
summary(fit.word_count)

stargazer(fit.ari, fit.coleman_liau, fit.flesch, fit.flesch_kincaid,
          fit.smog, fit.gunning_fog, fit.word_count, omit=c('year','state'),
          dep.var.labels = c('ARI','Coleman-Liau','Fleish','Fleish-Kincaid',
                            'SMOG','Gunning-Fog','Word Count'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))


## Model first factor in each state-year
fit.1f <- lm(paste('Factor1',selection.formula, sep='~'),
              data = year_state1d)
summary(fit.1f)
stargazer(fit.1f, omit=c('year','state'),
          dep.var.labels = c('Readability: First Factor'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))


## Model citations
fit.total.cites <- lm(paste('number_cites',selection.formula,sep='~'),
                      data = year_state1d)
summary(fit.total.cites)

fit.pos.cites <- lm(paste('pos_cites',selection.formula,sep='~'),
                      data = year_state1d)
summary(fit.pos.cites)

fit.neg.cites <- lm(paste('neg_cites',selection.formula,sep='~'),
                    data = year_state1d)
summary(fit.neg.cites)

stargazer(fit.total.cites, fit.pos.cites, fit.neg.cites, 
          omit=c('year','state'),
          dep.var.labels = c('Total Citations', 'Positive Citations', 
                             'Negative Citations'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))

# Poisson regression models of citations
fit.total.cites.pois <- glm(paste('number_cites',selection.formula,sep='~'),
                        data = year_state1d, family = poisson)
summary(fit.total.cites.pois)

fit.pos.cites.pois <- glm(paste('pos_cites',selection.formula,sep='~'),
                      data = year_state1d, family = poisson)
summary(fit.pos.cites.pois)

fit.neg.cites.pois <- glm(paste('neg_cites',selection.formula,sep='~'),
                      data = year_state1d, family = poisson)
summary(fit.neg.cites.pois)

stargazer(fit.total.cites.pois, fit.pos.cites.pois, fit.neg.cites.pois, 
          omit=c('year','state'),
          dep.var.labels = c('Total Citations', 'Positive Citations', 
                             'Negative Citations'),
          covariate.labels = c('Appointed', 'Retention Election', 
                               'Partisan Election', 'Caseload'))

# Logistic regression citations: does opinion cite a case?
year_state1d$cite.bi <- ifelse(year_state1d$number_cites > 0, 1, 0)
year_state1d$pos.cite.bi <- ifelse(year_state1d$pos_cites > 0, 1, 0)
year_state1d$neg_cite.bi <- ifelse(year_state1d$neg_cites > 0, 1, 0)

fit.total.cites.bi <- glm(paste('cite.bi',selection.formula,sep='~'),
                          data = year_state1d, family = 'binomial')
summary(fit.total.cites.bi)

fit.pos.cites.bi <- glm(paste('pos.cite.bi',selection.formula,sep='~'),
                          data = year_state1d, family = 'binomial')
summary(fit.pos.cites.bi)

fit.neg.cites.bi <- glm(paste('neg_cite.bi',selection.formula,sep='~'),
                          data = year_state1d, family = 'binomial')
summary(fit.neg.cites.bi)
