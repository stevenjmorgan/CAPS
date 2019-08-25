### This script applies PCA to the state court readability measures.

rm(list=ls())
#setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")
setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")

library(factoextra)
library(ggplot2)

# Read in data
state.courts <- read.csv('state_court_wide_final_bottom_half5-29.csv')
state.courts2 <- read.csv('state_court_wide_final_top_half5-30.csv')
all.courts <- rbind(state.courts,state.courts2)
save(all.courts, file = 'combined_read_metrics.RData')
#load('C:/Users/sum410/Downloads/combined_read_metrics.RData')
dim(all.courts)


# Subset dataset to only include opinions over over 50 words (removes 431,358 doc's)
over100 <- all.courts[which(all.courts$word_count > 50),]
over100 <- over100[which(over100$year >= 1776),]
dim(over100)
over100$state <- as.character(over100$state)

# Top states
top.states <- over100 %>%
  group_by(state) %>%
  summarize(n())
sum(top.states$`n()`) == nrow(over100)
top.states <- top.states[order(top.states$`n()`, decreasing = T),]
head(top.states)


# Omit na values, subset readability metrics
read.metrics <- na.omit(all.courts[,15:32])

# Deal w/ infinite values
read.metrics <- read.metrics[rowSums(is.infinite(as.matrix(read.metrics))) == 0,]
rm(state.courts,state.courts2)


## Summaries of each metric
#ARI
summary(all.courts$ARI_R)
summary(over100$ARI_R)
weird.case <- all.courts[which(all.courts$ARI_R > 800),]
less.than0 <- all.courts[which(all.courts$ARI_R < 0),]
remove.out <- all.courts[which(all.courts$ARI_R < 100),]
summary(remove.out$ARI_R)

# RIX
summary(all.courts$RIX_R)
summary(over100$RIX_R) # Same case producing max value for ARI and RIX (2 Blume Sup. Ct. Trans. 240)

# Coleman_Liau_Grade
summary(all.courts$Coleman_Liau_Grade_R)
summary(over100$Coleman_Liau_Grade_R) # Different case producing max values (81 Ohio St. (n.s.) 554 and 90 Ohio St. (n.s.) 404)

# Coleman-Liau Index
summary(all.courts$Coleman_Liau_Short_R)
summary(over100$Coleman_Liau_Short_R) # This may be the same as the grade (variable assign. error? Or intended result?)

# Danielson-Bryan
summary(all.courts$Danielson_Bryan_R)
summary(read.metrics$Danielson_Bryan_R)

# Dickes-Steiwer
summary(all.courts$Dickes_Steiwer_R)
summary(over100$Dickes_Steiwer_R)

# Easy Listening Formula
summary(all.courts$ELF_R)
summary(over100$ELF_R)
hist(over100$ELF_R[which(over100$ELF_R < 25)])

# Farr-Jenkins-Paterson's Simplification of Flesch's Reading Ease Score
summary(all.courts$Farr_Jenkins_Paterson_R)
summary(over100$Farr_Jenkins_Paterson_R)

# Flesch
summary(all.courts$flesch_R)
summary(over100$flesch_R)
hist(over100$flesch_R[which(over100$flesch_R > 0)])

# Flesch-Kincaid Readability Score
summary(all.courts$flesh_kincaid_R)
summary(over100$flesh_kincaid_R)
hist(over100$flesh_kincaid_R[which(over100$flesh_kincaid_R < 25)])

# FORCAST (Simplified Version of FORCAST.RGL) (Caylor and Sticht 1973)
summary(all.courts$FORCAST_R)
summary(over100$FORCAST_R)
hist(over100$flesh_kincaid_R[which(over100$flesh_kincaid_R < 25)])

# Fucks' (1955) Stilcharakteristik (Style Characteristic)
summary(all.courts$Fucks_R)
summary(over100$Fucks_R)
hist(over100$Fucks_R[which(over100$Fucks_R < 200)])

# FOG
summary(all.courts$FOG_R)
summary(over100$FOG_R)
hist(over100$FOG_R[which(over100$FOG_R < 30)])

# Linsear Write (Klare 1975)
summary(all.courts$Linsear_Write_R)
summary(over100$Linsear_Write_R)
hist(over100$Linsear_Write_R[which(over100$Linsear_Write_R < 30)])

#nWs 
summary(all.courts$nWS_R)
summary(over100$nWS_R)
hist(over100$nWS_R[which(over100$nWS_R < 15)])

# SMOG
summary(all.courts$SMOG_R)
summary(over100$SMOG_R)
hist(over100$SMOG_R[which(over100$SMOG_R < 30)])


### Remove outliers
all.courts <- all.courts[which(all.courts$flesch_R > -10 & all.courts$flesh_kincaid_R < 50 &
                           all.courts$ARI_R < 50 & all.courts$RIX_R < 30 & 
                           all.courts$Danielson_Bryan_R < 25 & all.courts$Dickes_Steiwer_R > -1000 &
                           all.courts$ELF_R < 50 & all.courts$Farr_Jenkins_Paterson_R > -300 &
                           all.courts$Fucks_R < 1000 & all.courts$FOG_R < 100 &
                           all.courts$Linsear_Write_R < 100 & all.courts$nWS_R < 50 &
                           all.courts$SMOG_R < 60),]

# Reverse scale Flesh and Flesh-Kincaid scores (so that large values indicate higher readability)
# new values = maximum value + minimum value - old values
hist(all.courts$flesch_R)
all.courts$flesch_R <- max(all.courts$flesch_R) + min(all.courts$flesch_R) - all.courts$flesch_R
hist(all.courts$flesch_R)

hist(all.courts$flesh_kincaid_R)
all.courts$flesh_kincaid_R <- max(all.courts$flesh_kincaid_R) + min(all.courts$flesh_kincaid_R) - all.courts$flesh_kincaid_R
hist(all.courts$flesh_kincaid_R)

# Only include cases with at least 100 words
all.courts <- all.courts[which(all.courts$word_count > 100),]
  
# Omit na values, subset readability metrics
read.metrics <- na.omit(all.courts[,15:32])

# Deal w/ infinte values
read.metrics <- read.metrics[rowSums(is.infinite(as.matrix(read.metrics))) == 0,] ### 1,624,698 cases
rm(state.courts,state.courts2) #,all.courts)

# Remove Coleman-Liau Short (quanteda does not calculate this correctly; it's the same as Coleman-Liau Grade)
read.metrics <- subset(read.metrics, select = -c(Coleman_Liau_Short_R))
dim(read.metrics)
colnames(read.metrics)


# Calculate singular value decomposition
read.pca <- prcomp(read.metrics, scale = TRUE)

# Visualize eigenvalues (scree plot)
fviz_eig(read.pca, ncp = 5, main = '')
ggsave('scree_plot_all_read_measures.png')

# Group by state, graph
#fviz_pca_var(read.pca,
#             col.var = "contrib", # Color by contributions to the PC
#             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
#             repel = TRUE     # Avoid text overlapping
#)

# Graph biplot correlation of variables
fviz_pca_var(read.pca,
             col.var = "contrib", # Color by contributions to the PC
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE     # Avoid text overlapping
)
ggsave('var_biplot_all_read_measures.png')

# Remove scientific notation
options(scipen=999)

### Access PCA results
# Eigenvalues
eig.val <- get_eigenvalue(read.pca) # First dimension explains 85.4% of variance
#eig.val

# Results for Variables
res.var <- get_pca_var(read.pca)
#res.var$coord          # Coordinates
#res.var$contrib        # Contributions to the PCs
#res.var$cos2           # Quality of representation 

# Results for individuals
res.ind <- get_pca_ind(read.pca)
#res.ind$coord          # Coordinates
#res.ind$contrib        # Contributions to the PCs
#res.ind$cos2           # Quality of representation 

# Pull first prin. component
coord <- as.data.frame(res.ind$coord[,1])
colnames(coord)[1] <- 'dim1'
summary(coord$dim1) # median = 0.3402; mean = 0
sd(coord$dim1) # 3.810639
hist(coord$dim1)#, xlim = c(-20,15))
hist(coord$dim1, xlim = c(-20, 20))


#coord <- as.data.frame(coord[which(coord$dim1 > -100),])
#colnames(coord)[1] <- 'dim1'
#summary(coord$dim1)

ggplot(coord, aes(x=dim1)) + geom_histogram(color="darkblue", fill="lightblue") +
  geom_vline(data=coord, aes(xintercept=median(dim1), color="red"),
             linetype="dashed") + xlim(-18, 18) + xlab('Dim. 1') + ylab('Count') + theme(legend.position='none')
ggsave('hist_1st_dim.png')


gc()



# Add first dim. values as variable
all.courts$first.dim <- coord$dim1
save(all.courts, file = 'firstdim.RData')


top.example <- all.courts[max(all.courts$first.dim),]
low.example <- all.courts[min(all.courts$first.dim),]
set.seed(24519)
low.example <- low.example[sample(nrow(low.example),1),]
low.example$word_count

ex <- mean(all.courts$first.dim) - sd(coord$dim1)
low.example <- all.courts[which(all.courts$first.dim < ex),]
low.example <- low.example[order(low.example$first.dim, decreasing = T),]
low.example <- low.example[which(low.example$word_count > 500),]
low.example <- low.example[7,]
low.example$cite

ex2 <- mean(all.courts$first.dim) + sd(coord$dim1)
top.example <- all.courts[which(all.courts$first.dim > ex2),]
top.example <- top.example[order(top.example$first.dim, decreasing = T),]
top.example <- top.example[which(top.example$word_count > 500),]
top.example <- top.example[4,]
top.example$cite


# Group by year-state median, sort by state
all.courts$state <- as.character(all.courts$state)
year_state1d <- aggregate(all.courts[,c('first.dim')], 
                           list(all.courts$state, all.courts$year), median)
colnames(year_state1d)[1] <- 'state'
colnames(year_state1d)[2] <- 'year'


# Plot first dimension measure by year and state
#load('firstdim.RData')
plot(year_state1d$year, year_state1d$x) # This is stupid, it's PCA, shouldn't plot aggregates
plot(all.courts$year, all.courts$x) # Lol this is dumber

ggplot(data=year_state1d, aes(x=year,y=x)) + geom_point()

summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  library(plyr)
  
  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }
  
  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=na.rm),
                     sd   = sd     (xx[[col]], na.rm=na.rm)
                   )
                 },
                 measurevar
  )
  
  # Rename the "mean" column    
  datac <- rename(datac, c("mean" = measurevar))
  
  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
  
  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval: 
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult
  
  return(datac)
}
tgc <- summarySE(all.courts[which(all.courts$state == 'Maryland'),], 
                 measurevar="first.dim" , groupvars=c("year"))

# Standard error of the mean
ggplot(tgc[which(tgc$year > 1775),], aes(x=year, y=first.dim)) + 
  geom_errorbar(aes(ymin=first.dim-se, ymax=first.dim+se), width=.1) +
  #geom_line() +
  geom_point() + xlab('Year') + ylab('Readability') +
  theme_bw() + 
  theme(text = element_text(size=25))
ggsave('MD_first_dim.png')
#ggplot(data=all.courts[which(all.courts$state == 'Massachusetts'),], aes(x=year,y=first.dim)) + geom_point()

tgc <- summarySE(all.courts, 
                 measurevar="first.dim" , groupvars=c("year"))
ggplot(tgc[which(tgc$year > 1775),], aes(x=year, y=first.dim)) + 
  geom_errorbar(aes(ymin=first.dim-se, ymax=first.dim+se), width=.1) +
  #geom_line() +
  geom_point() + xlab('Year') + ylab('Readability') +
  theme_bw() + 
  theme(text = element_text(size=25))
ggsave('all_years_first_dim.png')



# Standard error of the mean

###
load('combined_read_metrics.RData')

library(plyr)

all.courts$state <- as.character(all.courts$state)
freq <- plyr::count(all.courts, vars=c("year","state"))
year_state1d <- merge(year_state1d, freq, by = c('state','year'), all.x = TRUE)
year_state1d <- year_state1d[order(year_state1d$state, year_state1d$year),]
View(year_state1d)

save(year_state1d, file = 'year_state_measures.RData')



