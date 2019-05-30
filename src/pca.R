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

# Omit na values, subset readability metrics
read.metrics <- na.omit(all.courts[,15:32])

# Deal w/ infinte values
read.metrics <- read.metrics[rowSums(is.infinite(as.matrix(read.metrics))) == 0,]
rm(state.courts,state.courts2,all.courts)

# Calculate singular value decomposition
read.pca <- prcomp(read.metrics, scale = TRUE)

# Visualize eigenvalues (scree plot)
fviz_eig(read.pca)
ggsave('scree_plot_18.png')

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
ggsave('var_biplot.png')


### Access PCA results
# Eigenvalues
eig.val <- get_eigenvalue(read.pca)
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
summary(coord$dim1) # median = 0.0967; mean = 0
sd(coord$dim1) # 3.665649
hist(coord$dim1, xlim = c(-20,15))
hist(coord$dim1)

coord <- as.data.frame(coord[which(coord$dim1 > -100),])
colnames(coord)[1] <- 'dim1'
summary(coord$dim1)

ggplot(coord, aes(x=dim1)) + geom_histogram()
