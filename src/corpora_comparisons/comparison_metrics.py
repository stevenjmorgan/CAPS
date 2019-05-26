# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:26:16 2019

Run readability measures on ``baseline corpora'' to compare CAPS metrics

@author: steve
"""

import textstat
import pandas as pd
import os
from rpy2.robjects.packages import importr
import nltk
from nltk.corpus import gutenberg

def read_metrics(text_clean):
    
    table = {}
    
    #table['flesch'] = textstat.flesch_reading_ease(text_clean)
    #table['flesch_kincaid'] = textstat.flesch_kincaid_grade(text_clean)
    table['fog'] = textstat.gunning_fog(text_clean)
    table['smog'] = textstat.smog_index(text_clean)
    table['ari'] = textstat.automated_readability_index(text_clean)
    table['coleman_liau'] = textstat.coleman_liau_index(text_clean)

    r_read_mets = quanteda.textstat_readability(text_clean, measure = 'all')
    table['ari_r'] = float(r_read_mets[1].r_repr())
    table['rix_r'] = float(r_read_mets[35].r_repr())
    table['Coleman_Liau_Grade_R'] = float(r_read_mets[9].r_repr())
    table['Coleman_Liau_Short_R'] = float(r_read_mets[10].r_repr())
    table['Danielson_Bryan_R'] = float(r_read_mets[14].r_repr())
    table['Dickes_Steiwer_R'] = float(r_read_mets[16].r_repr())
    table['ELF_R'] = float(r_read_mets[18].r_repr())
    table['Farr_Jenkins_Paterson_R'] = float(r_read_mets[19].r_repr())
    table['flesch_R'] = float(r_read_mets[20].r_repr())
    table['flesh_kincaid_R'] = float(r_read_mets[22].r_repr())
    table['FORCAST_R'] = float(r_read_mets[26].r_repr())
    table['Fucks_R'] = float(r_read_mets[28].r_repr())
    table['FOG_R'] = float(r_read_mets[23].r_repr())
    table['Linsear_Write_R'] = float(r_read_mets[29].r_repr())
    table['nWS_R'] = float(r_read_mets[31].r_repr())
    table['SMOG_R'] = float(r_read_mets[37].r_repr())
    table['Strain_R'] = float(r_read_mets[43].r_repr())
    table['Wheeler_Smith_R'] = float(r_read_mets[46].r_repr())
                    
    return table


# Set working directory
os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
#os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

#nltk.download() # Opens download window -> click ``Download all'' button
    
# Import quanteda from R
# In R: install.packages("lattice", lib="C:/Users/steve/Anaconda3/Lib/R/library", dependencies=TRUE)
quanteda = importr("quanteda", lib_loc = "C:/Users/steve/OneDrive/Documents/R/win-library/3.5")
#quanteda = importr("quanteda", lib_loc = "C:/Users/sum410/Documents/R/R-3.5.2/library") 
#quanteda = importr("quanteda", lib_loc = "C:/Program Files/R/R-3.5.1/library")

#gutenberg.fileids()
moby = gutenberg.raw('melville-moby_dick.txt')
genesis = nltk.corpus.genesis.raw('english-kjv.txt')

# Clean text
moby = moby.replace('\n','').replace('\t','')
genesis = genesis.replace('\n','').replace('\t','')

# Number of words in Moby Dick and Genesis
len(moby)
len(genesis)

# Run readability analysis
moby_read = read_metrics(moby)
gen_read = read_metrics(genesis)

# Convert to dataframe
read_df = pd.DataFrame([moby_read, gen_read])
read_df.to_csv('corpora_comparisons.csv')
