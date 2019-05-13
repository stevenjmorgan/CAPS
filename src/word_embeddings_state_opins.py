# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:44:44 2019

@author: sum410
"""

import os, warnings, gensim, nltk, multiprocessing
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

warnings.filterwarnings(action = 'ignore')

