### This script applies PCA to the state court readability measures.

rm(list=ls())
setwd("C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP")
#setwd("C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP")

library(factoextra)
library(ggplot2)

# Read in data
state.courts <- read.csv('state_court_wide_final_bottom_half5-29.csv')
state.courts2 <- read.csv('state_court_wide_final_top_half5-30.csv')
all.courts <- rbind(state.courts,state.courts2)

# Subset dataset to only include opinions over over 100 words (removes 431,358 doc's)
over100 <- all.courts[which(all.courts$word_count > 100),]

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
