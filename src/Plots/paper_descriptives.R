# This script creates figures and plots for the paper from the dataset.

rm(list=ls())
setwd('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP')

library(ggplot2)
library(maps)
library(mapdata)
library(mapproj)
library(tidyverse)
library(devtools)
devtools::install_github("UrbanInstitute/urbnmapr")
library(urbnmapr)
#library(usmap)

# Read in data
wide <- read.csv('state_court_wide_final4-12.csv')
colnames(wide)
head(wide)
#wide <- wide[which(wide$decade >= 1770),]
wide <- wide[which(wide$year >= 1776),]
wide <- wide[which(wide$word_count > 50),]
load('C:/Users/sum410/Downloads/combined_read_metrics.RData')

# Subset dataset to only include opinions over over 50 words (removes 431,358 doc's)
over100 <- all.courts[which(all.courts$word_count > 50),]
over100 <- over100[which(over100$year >= 1776),]
dim(over100)
over100$state <- as.character(over100$state)
wide <- over100

#long <- read.csv('state_court_long_final.csv')
#colnames(long)
#head(long)

# Create region variable with lowercase state names
wide$region <- tolower(wide$state)
unique(wide$region)

# Courts in dataset
length(unique(wide$court))

# Group cases by state
group.state <- wide %>% group_by(region) %>%
  summarise(trues = n())
colnames(group.state)[colnames(group.state) == 'trues'] <- 'total.cases'

group.state <- group.state[order(group.state$total.cases, decreasing = TRUE),]

# Create map of states based on # of cases
us <- map_data('state')

# Plot
ggplot() + geom_map(data=us, map=us, aes(long, lat, map_id=region), color="#2b2b2b", fill=NA, size=0.15) +
  geom_map(data=group.state, map=us, aes(fill=total.cases, map_id=region), color="#ffffff", size=0.15) + labs(x=NULL, y=NULL) +
  scale_fill_continuous(low='gray80', high='gray20',  guide='colorbar') +
  theme(panel.border = element_blank(), panel.background = element_blank(), 
        plot.title = element_text(hjust = 0.5,size = 25, face = "bold"), axis.ticks = element_blank(),
        axis.text = element_blank()) + guides(fill = guide_colorbar(title=NULL)) + coord_map() + 
  ggtitle("Number of Cases by State: 1776-2018")
ggsave('cases_state.png')

# Plot post 1950
post1950 <- over100[which(over100$year > 1949),]
group.state1950 <- post1950 %>% group_by(state) %>%
  summarise(trues = n())
colnames(group.state1950)[colnames(group.state1950) == 'trues'] <- 'total.cases'
colnames(group.state1950)[colnames(group.state1950) == 'state'] <- 'region'
group.state1950$region <- tolower(group.state1950$region)
ggplot() + geom_map(data=us, map=us, aes(long, lat, map_id=region), color="#2b2b2b", fill=NA, size=0.15) +
  geom_map(data=group.state1950, map=us, aes(fill=total.cases, map_id=region), color="#ffffff", size=0.15) + labs(x=NULL, y=NULL) +
  scale_fill_continuous(low='gray80', high='gray20',  guide='colorbar') +
  theme(panel.border = element_blank(), panel.background = element_blank(), 
        plot.title = element_text(hjust = 0.5,size = 25, face = "bold"), axis.ticks = element_blank(),
        axis.text = element_blank()) + guides(fill = guide_colorbar(title=NULL)) + coord_map() + 
ggtitle("Number of Cases by State: 1950-2017")
ggsave('cases_state_1950.png')

# Group by year
group.year <- over100 %>% group_by(year) %>%
  summarise(trues = n())
colnames(group.year)[colnames(group.year) == 'trues'] <- 'total.cases'

group.year <- group.year[order(group.year$year, decreasing = T),]



# Merge
library(datasets)
state.abb
states <- states
states$state_name <- tolower(states$state_name)
group.state <- left_join(group.state, states,  by = c('region' = 'state_name'))

group.state %>%
  ggplot(aes(long, lat, group = group, fill = total.cases)) +
  geom_polygon(color = NA) +
  coord_map(projection = "albers", lat0 = 39, lat1 = 45) +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank()) +
  labs(fill = "Total Cases")
ggsave('cases_state_al_hi.png',  width = 8, height = 5)

# Group cases by state since 1950
wide.1950 <- wide[which(wide$year >= 1950),]
group.state.1950 <- wide.1950 %>% group_by(region) %>%
  summarise(trues = n())
colnames(group.state.1950)[colnames(group.state.1950) == 'trues'] <- 'total.cases'

group.state.1950 <- left_join(group.state.1950, states,  by = c('region' = 'state_name'))

options(scipen=999)
group.state.1950 %>%
  ggplot(aes(long, lat, group = group, fill = total.cases)) +
  geom_polygon(color = NA) +
  coord_map(projection = "albers", lat0 = 39, lat1 = 45) +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.title.y=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank()) +
  labs(fill = "Total Cases since 1950")
ggsave('cases_state_al_hi_post1950.png', width = 8, height = 5)


# Group and plot by decade
group.dec <- over100 %>% group_by(decade) %>%
  summarise(trues = n())
colnames(group.dec)[colnames(group.dec) == 'trues'] <- 'total.cases'
ggplot(group.dec, aes(x=decade, y=total.cases)) + geom_point() +
  xlab('Decade') + ylab('Cases') + theme_bw()
ggsave('cases_decade.png')       

# Group and plot by year
group.yr <- wide %>% group_by(year) %>%
  summarise(trues = n())
colnames(group.yr)[colnames(group.yr) == 'trues'] <- 'total.cases'
ggplot(group.yr, aes(x=year, y=total.cases)) + geom_point() +
  xlab('Year') + ylab('Cases') + theme_bw()
ggsave('cases_year.png')


# Group and plot by year
wc.yr <- wide %>% group_by(year) %>%
  summarise(mean(word_count))
colnames(wc.yr)[colnames(wc.yr) == 'mean(word_count)'] <- 'average_wc'
ggplot(wc.yr, aes(x=year, y=average_wc)) + geom_point() +
  xlab('Year') + ylab('Average Word Count') + theme_bw()
ggsave('average_wc.png')

wc.dec <- wide %>% group_by(decade) %>%
  summarise(mean(word_count))
colnames(wc.dec)[colnames(wc.dec) == 'mean(word_count)'] <- 'average_wc'
ggplot(wc.dec, aes(x=decade,y=average_wc)) + geom_point() +
  xlab('Decade') + ylab('Average Word Count') + theme_bw()
ggsave('average_wc_dec.png')
