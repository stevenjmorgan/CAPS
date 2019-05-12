# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:06:10 2019

@author: steve
"""

import rpy2.rinterface
from rpy2.robjects.packages import importr
#from rpy2.robjects.packages import importr

base = importr('base')
print(base._libPaths()) #[1] "C:/Users/steve/Anaconda3/Lib/R/library"

quanteda = importr("quanteda", lib_loc = "C:/Users/steve/OneDrive/Documents/R/win-library/3.5")