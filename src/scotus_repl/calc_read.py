# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:05:27 2019

@author: sum410
"""

import pandas as pd
import re
import os
import glob
import json
import textstat
from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work
import rpy2.rinterface
from rpy2.robjects.packages import importr

# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))

# Import quanteda from R
# In R: install.packages("lattice", lib="C:/Users/steve/Anaconda3/Lib/R/library", dependencies=TRUE)
#quanteda = importr("quanteda", lib_loc = "C:/Users/steve/OneDrive/Documents/R/win-library/3.5")
quanteda = importr("quanteda", lib_loc = "C:/Users/sum410/Documents/R/R-3.5.2/library") 


# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

scotus = pd.read_csv('scotus_subset.csv', encoding = "ISO-8859-1")

for index, row in scotus.iterrows():
    print(row['opin_text'])
    
    try:
        r_read_mets = quanteda.textstat_readability(row['opin_text'], measure = 'all')
        
        ari_r = float(r_read_mets[1].r_repr())
        rix_r = float(r_read_mets[35].r_repr())
        Coleman_Liau_Grade_R = float(r_read_mets[9].r_repr())
        Coleman_Liau_Short_R = float(r_read_mets[10].r_repr())
        Danielson_Bryan_R = float(r_read_mets[14].r_repr())
        Dickes_Steiwer_R = float(r_read_mets[16].r_repr())
        ELF_R = float(r_read_mets[18].r_repr())
        Farr_Jenkins_Paterson_R = float(r_read_mets[19].r_repr())
        flesch_R = float(r_read_mets[20].r_repr())
        flesh_kincaid_R = float(r_read_mets[22].r_repr())
        FORCAST_R = float(r_read_mets[26].r_repr())
        Fucks_R = float(r_read_mets[28].r_repr())
        FOG_R = float(r_read_mets[23].r_repr())
        Linsear_Write_R = float(r_read_mets[29].r_repr())
        nWS_R = float(r_read_mets[31].r_repr())
        SMOG_R = float(r_read_mets[37].r_repr())
        Strain_R = float(r_read_mets[43].r_repr())
        Wheeler_Smith_R = float(r_read_mets[46].r_repr())
    except:
        pass



