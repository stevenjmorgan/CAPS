### This script applies PCA to the US corpus readability measures.

rm(list=ls())
setwd('C:/Users/SF515-51T/Desktop/CAPS')

library(factoextra)
library(ggplot2)
library(dplyr)
library(plyr)

# Read in data
corpus <- read.csv('benchmark_readability.csv')
dim(corpus)

# Plot # of observations by year/decade
summary(corpus$word_count)
corp.yr <- corpus %>% dplyr::count(year)
corpus$decade <- round_any(corpus$year,10, f = floor)
corp.dec <- corpus %>% dplyr::count(decade)
plot(corp.yr$year, corp.yr$n)
plot(corp.dec$decade, corp.dec$n)
ggplot(corp.yr, aes(x=year, y=n)) + geom_point() + ylab('Number of documents') +
  xlab('') + ggtitle('Number of Documents by Year: US Corpus')
ggsave('docs_year_us_corpus.png')
ggplot(corp.dec, aes(x=decade, y=n)) + geom_point() + ylab('Number of documents') +
  xlab('') + ggtitle('Number of Documents by Decade: US Corpus')
ggsave('docs_dec_us_corpus.png')

# Omit na values, subset readability metrics
colnames(corpus)
read.metrics <- na.omit(corpus[,1:18])
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'file_id')]
colnames(read.metrics)

# Deal w/ infinite values
read.metrics <- read.metrics[rowSums(is.infinite(as.matrix(read.metrics))) == 0,]

# Reverse scale Flesh and Flesh-Kincaid scores (so that large values indicate higher readability)
# new values = maximum value + minimum value - old values
# hist(read.metrics$flesch_R)
# read.metrics$flesch_R <- max(read.metrics$flesch_R) + min(read.metrics$flesch_R) - read.metrics$flesch_R
# hist(read.metrics$flesch_R)

# Remove Coleman-Liau Short (quanteda does not calculate this correctly; it's the same as Coleman-Liau Grade)
read.metrics <- subset(read.metrics, select = -c(Coleman_Liau_Short_R))
dim(read.metrics)
colnames(read.metrics)

# Calculate singular value decomposition
read.pca <- prcomp(read.metrics, scale = TRUE)

# Visualize eigenvalues (scree plot)
fviz_eig(read.pca, ncp = 5, main = 'Scree Plot: US Corpus Benchmark')
ggsave('scree_plot_benchmark_measures.png')

# Graph biplot correlation of variables
fviz_pca_var(read.pca,
             col.var = "contrib", # Color by contributions to the PC
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE     # Avoid text overlapping
)
ggsave('var_biplot_us_benchmark_measures.png')

# Remove scientific notation
options(scipen=999)

### Access PCA results
# Eigenvalues
eig.val <- get_eigenvalue(read.pca)
eig.val # First dimension explains 86.5% of variance

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
summary(coord$dim1) # median = -0.1951; mean = 0
sd(coord$dim1) # 3.721
hist(coord$dim1)#, xlim = c(-20,15))
hist(coord$dim1, xlim = c(-20, 20))


#coord <- as.data.frame(coord[which(coord$dim1 > -100),])
#colnames(coord)[1] <- 'dim1'
#summary(coord$dim1)

ggplot(coord, aes(x=dim1)) + geom_histogram(color="darkblue", fill="lightblue") +
  geom_vline(data=coord, aes(xintercept=median(dim1), color="red"),
             linetype="dashed") + xlim(-18, 18) + xlab('Dim. 1') + ylab('Count') + theme(legend.position='none')
#ggsave('hist_1st_dim.png')

gc()

# Add first dim. values as variable
corpus$first.dim <- coord$dim1


# top.example <- all.courts[max(all.courts$first.dim),]
# low.example <- all.courts[min(all.courts$first.dim),]
# set.seed(24519)
# low.example <- low.example[sample(nrow(low.example),1),]
# low.example$word_count
# 
# ex <- mean(all.courts$first.dim) - sd(coord$dim1)
# low.example <- all.courts[which(all.courts$first.dim < ex),]
# low.example <- low.example[order(low.example$first.dim, decreasing = T),]
# low.example <- low.example[which(low.example$word_count > 500),]
# low.example <- low.example[7,]
# low.example$cite
# 
# ex2 <- mean(all.courts$first.dim) + sd(coord$dim1)
# top.example <- all.courts[which(all.courts$first.dim > ex2),]
# top.example <- top.example[order(top.example$first.dim, decreasing = T),]
# top.example <- top.example[which(top.example$word_count > 500),]
# top.example <- top.example[4,]
# top.example$cite


# Group by year/decade median
year.1d <- aggregate(corpus[,c('first.dim')], 
                          list(corpus$year), median)
colnames(year.1d)[1] <- 'year'
dec.1d <- aggregate(corpus[,c('first.dim')], 
                    list(corpus$decade), median)
colnames(dec.1d)[1] <- 'decade'


# Plot first dimension measure by year and state
#load('firstdim.RData')
plot(year_state1d$year, year_state1d$x) # This is stupid, it's PCA, shouldn't plot aggregates
plot(all.courts$year, all.courts$x) # Lol this is dumber

ggplot(data=year.1d, aes(x=year,y=x)) + geom_point()

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
tgc <- summarySE(corpus, 
                 measurevar="first.dim" , groupvars=c("year"))

# Standard error of the mean
ggplot(tgc, aes(x=year, y=first.dim)) + 
  geom_errorbar(aes(ymin=first.dim-se, ymax=first.dim+se), width=.1) +
  #geom_line() +
  geom_point() + xlab('Year') + ylab('Readability') +
  theme_bw() + ggtitle('PCA Readability Scores by Year: US Benchmark Corpus')
ggsave('year_benchmark_first_dim.png')
#ggplot(data=all.courts[which(all.courts$state == 'Massachusetts'),], aes(x=year,y=first.dim)) + geom_point()


# Decade
tgc <- summarySE(corpus, 
                 measurevar="first.dim" , groupvars=c("decade"))

# Standard error of the mean
ggplot(tgc, aes(x=decade, y=first.dim)) + 
  geom_errorbar(aes(ymin=first.dim-se, ymax=first.dim+se), width=.1) +
  #geom_line() +
  geom_point() + xlab('Decade') + ylab('Readability') +
  theme_bw() + ggtitle('PCA Readability Scores by Decade: US Benchmark Corpus')
ggsave('dec_benchmark_first_dim.png')
#ggplot(data=all.courts[which(all.courts$state == 'Massachusetts'),], aes(x=year,y=first.dim)) + geom_point()

save(year.1d, file = 'byu_read.RData')