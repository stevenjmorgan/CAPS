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
wide <- read.csv('state_court_wide_final.csv')
colnames(wide)
head(wide)

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
ggsave('cases_state_al_hi.png')
