# This script creates figures and plots for the paper from the dataset.

rm(list=ls())
setwd('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP')

library(ggplot2)
library(maps)
library(mapdata)
library(mapproj)
library(tidyverse)
library(urbnmapr)
#library(usmap)

# Read in data
wide <- read.csv('state_court_wide_final4-12.csv')
colnames(wide)
head(wide)
#wide <- wide[which(wide$decade >= 1770),]
wide <- wide[which(wide$year >= 1776),]

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
  ggtitle("Number of Cases by State")
ggsave('cases_state.png')

# Merge
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
group.dec <- wide %>% group_by(decade) %>%
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
