# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:24:44 2019

@author: sum410
"""

import rpy2.rinterface
from rpy2.robjects.packages import importr
import time, nltk

quanteda = importr("quanteda", lib_loc = "C:/Users/sum410/Documents/R/R-3.5.2/library") 

nltk.download('gutenberg')
nltk.corpus.gutenberg.fileids()
text_clean = nltk.corpus.gutenberg.raw('melville-moby_dick.txt')

start = time.time()
ari_r = float(quanteda.textstat_readability(text_clean, measure = 'ARI')[1].r_repr())
rix_r = float(quanteda.textstat_readability(text_clean, measure = 'RIX')[1].r_repr())
Coleman_Liau_Grade_R = float(quanteda.textstat_readability(text_clean, measure = 'Coleman.Liau.grade')[1].r_repr())
Coleman_Liau_Short_R = float(quanteda.textstat_readability(text_clean, measure = 'Coleman.Liau.short')[1].r_repr())
Danielson_Bryan_R = float(quanteda.textstat_readability(text_clean, measure = 'Danielson.Bryan')[1].r_repr())
Dickes_Steiwer_R = float(quanteda.textstat_readability(text_clean, measure = 'Dickes.Steiwer')[1].r_repr())
ELF_R = float(quanteda.textstat_readability(text_clean, measure = 'ELF')[1].r_repr())
Farr_Jenkins_Paterson_R = float(quanteda.textstat_readability(text_clean, measure = 'Farr.Jenkins.Paterson')[1].r_repr())
flesch_R = float(quanteda.textstat_readability(text_clean, measure = 'Flesch')[1].r_repr())
flesh_kincaid_R = float(quanteda.textstat_readability(text_clean, measure = 'Flesch.Kincaid')[1].r_repr())
FORCAST_R = float(quanteda.textstat_readability(text_clean, measure = 'FORCAST')[1].r_repr())
Fucks_R = float(quanteda.textstat_readability(text_clean, measure = 'Fucks')[1].r_repr())
FOG_R = float(quanteda.textstat_readability(text_clean, measure = 'FOG')[1].r_repr())
Linsear_Write_R = float(quanteda.textstat_readability(text_clean, measure = 'Linsear.Write')[1].r_repr())
nWS_R = float(quanteda.textstat_readability(text_clean, measure = 'nWS')[1].r_repr())
SMOG_R = float(quanteda.textstat_readability(text_clean, measure = 'SMOG')[1].r_repr())
Strain_R = float(quanteda.textstat_readability(text_clean, measure = 'Strain')[1].r_repr())
Wheeler_Smith_R = float(quanteda.textstat_readability(text_clean, measure = 'Wheeler.Smith')[1].r_repr())
end = time.time()
print(end - start)


start = time.time()
x = quanteda.textstat_readability(text_clean, measure = 'all')
end = time.time()
print(end - start)


x[46].r_repr()
