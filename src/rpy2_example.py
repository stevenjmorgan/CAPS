# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:06:10 2019

@author: steve
"""

import rpy2.rinterface
from rpy2.robjects.packages import importr
#from rpy2.robjects.packages import importr

base = importr('base', lib_loc = "C:/Users/steve/OneDrive/Documents/R/win-library/3.5")
print(base._libPaths()) #[1] "C:/Users/steve/Anaconda3/Lib/R/library"


# In R: install.packages("lattice", lib="C:/Users/steve/Anaconda3/Lib/R/library", dependencies=TRUE)
quanteda = importr("quanteda", lib_loc = "C:/Users/steve/OneDrive/Documents/R/win-library/3.5")
#quanteda.chooseCRANmirror(ind=1)

x = quanteda.textstat_readability('The house is cool', measure = 'ARI')[1]
x.r_repr()

type(quanteda.textstat_readability('The house is cool', measure = 'ARI')[1].r_repr())
ari_score = float(quanteda.textstat_readability('The house is cool', measure = 'ARI')[1].r_repr())