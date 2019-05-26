# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:26:16 2019

Run readability measures on ``baseline corpora'' to compare CAPS metrics

@author: steve
"""

import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work
import pandas as pd
import numpy as np
import re, time
import os
import glob
import pickle
import rpy2.rinterface
from rpy2.robjects.packages import importr
import nltk
from nltk.book import *

#nltk.download() # Opens download window -> click ``Download all'' button

text1



flesch = textstat.flesch_reading_ease(text_clean)
flesch_kincaid = textstat.flesch_kincaid_grade(text_clean)
fog = textstat.gunning_fog(text_clean)
smog = textstat.smog_index(text_clean)
ari = textstat.automated_readability_index(text_clean)
coleman_liau = textstat.coleman_liau_index(text_clean)

