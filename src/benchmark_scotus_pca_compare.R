### This script conducts PCA on SCOTUS readability measure and compares to
### the BYU lingustics corpus and State Supreme Court readability measures

rm(list=ls())
setwd('C:/Users/SF515-51T/Desktop/CAPS')

library(factoextra)
library(ggplot2)
library(dplyr)
library(plyr)

scotus <- read.csv('benchmark_SCOTUS_readability_v2.csv')
colnames(scotus)
length(unique(scotus$cite))

# De-duplicate SCOTUS cases, remove opinions w/ less than 50 words
scotus <- scotus[which(scotus$word_count >= 50),]
scotus <- scotus[!duplicated(scotus$cite),]
scotus <- scotus[which(scotus$year <= 2015),]

# Count cases by year
class(scotus$year)
length(unique(scotus$year))
scotus.yr <- scotus %>% dplyr::count(year)
rm(scotus.yr)
scotus$decade <- round_any(scotus$year,10, f = floor)

# Omit na values, subset readability metrics
read.metrics <- na.omit(scotus[,1:23])
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'file_id')]
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'cite')]
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'court')]
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'date')]
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'has_opinion')]
read.metrics <- read.metrics[,which(colnames(read.metrics) != 'case')]
colnames(read.metrics)

# Deal w/ infinite values
read.metrics <- read.metrics[rowSums(is.infinite(as.matrix(read.metrics))) == 0,]

# Remove Coleman-Liau Short (quanteda does not calculate this correctly; it's the same as Coleman-Liau Grade)
read.metrics <- subset(read.metrics, select = -c(Coleman_Liau_Short_R))
dim(read.metrics)
colnames(read.metrics)

# Calculate singular value decomposition
read.pca <- prcomp(read.metrics, scale = TRUE)

# Visualize eigenvalues (scree plot)
fviz_eig(read.pca, ncp = 5, main = 'Scree Plot: SCOTUS Benchmark')
ggsave('scree_plot_scotus_measures.png')

# Graph biplot correlation of variables
fviz_pca_var(read.pca,
             col.var = "contrib", # Color by contributions to the PC
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE     # Avoid text overlapping
)
ggsave('var_biplot_scotus_benchmark_measures.png')

# Remove scientific notation
options(scipen=999)

### Access PCA results
# Eigenvalues
eig.val <- get_eigenvalue(read.pca)
eig.val # First dimension explains 85.5% of variance

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
summary(coord$dim1) # median = -0.2619; mean = 0
sd(coord$dim1) # 3.813
hist(coord$dim1)#, xlim = c(-20,15))
hist(coord$dim1, xlim = c(-20, 20))

ggplot(coord, aes(x=dim1)) + geom_histogram(color="darkblue", fill="lightblue") +
  geom_vline(data=coord, aes(xintercept=median(dim1), color="red"),
             linetype="dashed") + xlim(-18, 18) + xlab('Dim. 1') + ylab('Count') + theme(legend.position='none')
#ggsave('hist_1st_dim.png')

gc()

# Add first dim. values as variable
scotus$first.dim <- coord$dim1

# Group by year/decade median
year.1d <- aggregate(scotus[,c('first.dim')], 
                     list(scotus$year), median)
colnames(year.1d)[1] <- 'year'
dec.1d <- aggregate(scotus[,c('first.dim')], 
                    list(scotus$decade), median)
colnames(dec.1d)[1] <- 'decade'

### Plots
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
tgc <- summarySE(scotus, 
                 measurevar="first.dim" , groupvars=c("year"))

# Standard error of the mean
ggplot(tgc, aes(x=year, y=first.dim)) + 
  geom_errorbar(aes(ymin=first.dim-se, ymax=first.dim+se), width=.1) +
  #geom_line() +
  geom_point() + xlab('Year') + ylab('Readability') +
  theme_bw() + ggtitle('PCA Readability Scores by Year: US Benchmark Corpus')
ggsave('year_scotus_benchmark_first_dim.png')
#ggplot(data=all.courts[which(all.courts$state == 'Massachusetts'),], aes(x=year,y=first.dim)) + geom_point()
