# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 13:54:22 2020

@author: SF515-51T
"""

import spacy
#from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work
from datetime import datetime
import json
#import numpy as np 
import pandas as pd
import numpy as np
import re, time
import os
import glob
import sys
import pickle
#from ggplot import aes
#from ggplot import ggplot
import matplotlib.pyplot as plt
import textstat
#import matplotlib.backends.backend_pdf
#import timeit
#import lexnlp.extract.en.citations
#import lexnlp.nlp.en.segments.sentences
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import rpy2.rinterface
from rpy2.robjects.packages import importr
import rpy2.robjects as ro


# Splits the text into sentences, using  
# Spacy's sentence segmentation which can  
# be found at https://spacy.io/usage/spacy-101 
def break_sentences(text): 
    #nlp = spacy.load('en') #``python -m spacy download'' in command line
    nlp = spacy.load('en_core_web_sm') # if user lacks admin. priviledges
    doc = nlp(text) 
    return doc.sents 
   
# Returns Number of Words in the text 
def word_count(text): 
    sentences = break_sentences(text) 
    words = 0
    for sentence in sentences: 
        words += len([token for token in sentence]) 
    return words 
   
# Returns the number of sentences in the text 
def sentence_count(text): 
    sentences = break_sentences(text) 
    return len(sentences) 
   
# Returns average sentence length 
def avg_sentence_length(text): 
    words = word_count(text) 
    sentences = sentence_count(text) 
    average_sentence_length = float(words / sentences) 
    return average_sentence_length 
   
# Textstat is a python package, to calculate statistics from  
# text to determine readability,  
# complexity and grade level of a particular corpus. 
# Package can be found at https://pypi.python.org/pypi/textstat 
def syllables_count(word): 
    return textstatistics().syllable_count(word) 
   
# Returns the average number of syllables per 
# word in the text 
    syllable = syllables_count(text) 
    words = word_count(text) 
def avg_syllables_per_word(text): 
    ASPW = float(syllable) / float(words) 
    return legacy_round(ASPW, 1) 
   
# Return total Difficult Words in a text 
def difficult_words(text): 
   
    # Find all words in the text 
    words = [] 
    sentences = break_sentences(text) 
    for sentence in sentences: 
        words += [str(token) for token in sentence] 
   
    # difficult words are those with syllables >= 2 
    # easy_word_set is provide by Textstat as  
    # a list of common words 
    diff_words_set = set() 
       
    for word in words: 
        syllable_count = syllables_count(word) 
        if word not in easy_word_set and syllable_count >= 2: 
            diff_words_set.add(word) 
   
    return len(diff_words_set) 
   
# A word is polysyllablic if it has more than 3 syllables 
# this functions returns the number of all such words  
# present in the text 
def poly_syllable_count(text): 
    count = 0
    words = [] 
    sentences = break_sentences(text) 
    for sentence in sentences: 
        words += [token for token in sentence] 
       
   
    for word in words: 
        syllable_count = syllables_count(word) 
        if syllable_count >= 3: 
            count += 1
    return count 
      
def flesch_reading_ease(text): 
    """ 
        Implements Flesch Formula: 
        Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW) 
        Here, 
          ASL = average sentence length (number of words  
                divided by number of sentences) 
          ASW = average word length in syllables (number of syllables  
                divided by number of words) 
    """
    FRE = 206.835 - float(1.015 * avg_sentence_length(text)) - float(84.6 * avg_syllables_per_word(text)) 
    return legacy_round(FRE, 2) 
      
def gunning_fog(text): 
    per_diff_words = (difficult_words(text) / word_count(text) * 100) + 5
    grade = 0.4 * (avg_sentence_length(text) + per_diff_words) 
    return grade 
   
def smog_index(text): 
    """ 
        Implements SMOG Formula / Grading 
        SMOG grading = 3 + ?polysyllable count. 
        Here,  
           polysyllable count = number of words of more 
          than two syllables in a sample of 30 sentences. 
    """
   
    if sentence_count(text) >= 3: 
        poly_syllab = poly_syllable_count(text) 
        SMOG = (1.043 * (30*(poly_syllab / sentence_count(text)))**0.5) + 3.1291
        return legacy_round(SMOG, 1) 
    else: 
        return 0
   
def dale_chall_readability_score(text): 
    """ 
        Implements Dale Challe Formula: 
        Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365 
        Here, 
            PDW = Percentage of difficult words. 
            ASL = Average sentence length 
    """
    words = word_count(text) 
    # Number of words not termed as difficult words 
    count = word_count - difficult_words(text) 
    if words > 0: 
   
        # Percentage of words not on difficult word list 
   
        per = float(count) / float(words) * 100
       
    # diff_words stores percentage of difficult words 
    diff_words = 100 - per 
   
    raw_score = (0.1579 * diff_words) + (0.0496 * avg_sentence_length(text)) 
       
    # If Percentage of Difficult Words is greater than 5 %, then; 
    # Adjusted Score = Raw Score + 3.6365, 
    # otherwise Adjusted Score = Raw Score 
   
    if diff_words > 5:        
   
        raw_score += 3.6365
           
    return legacy_round(raw_score, 2)  #score


# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
#os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir(r'C:\Users\SF515-51T\Desktop\CAPS')


#files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/','*.*')))
files = list(glob.glob(os.path.join('C:/Users/SF515-51T/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data','*.*')))
#states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.split('C:/Users/SF515-51T/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.replace("\\", "") for x in states]
states = [x.replace(".jsonl", "") for x in states]
files[0] = files[0].replace('\\', '/')

state_high_list = ['United States Supreme Court', 
                   'Supreme Court of United States',
                   'United State Supreme Court',
                   'Supreme Court of the United States']

case_list = pd.read_csv('scotus_cases.csv', index_col=False)
case_list = case_list['cases'].to_list()
case_list = (list(set(case_list)))

# Import quanteda from R
quanteda = importr('quanteda')

# Create dictionary to store results
file_d = {}
columns = ['file_id', 'year', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'number_cites', 'citations',
           'pos_cites', 'neg_cites', 'has_opinion', 'total_opins', 'greater50',
           'opin_author', 'judges', 'sentence_len', 'sentence_30', 
           'ARI_R', 'RIX_R', 'Coleman_Liau_Grade_R', 'Coleman_Liau_Short_R',
           'Danielson_Bryan_R', 'Dickes_Steiwer_R', 'ELF_R', 
           'Farr_Jenkins_Paterson_R', 'flesch_R', 'flesh_kincaid_R',
           'FORCAST_R', 'Fucks_R', 'FOG_R', 'Linsear_Write_R', 'nWS_R', 
           'SMOG_R', 'Strain_R', 'Wheeler_Smith_R']

rows_list = []
with open(files[0]) as f:

    for line in f:
        
        data = json.loads(line)
        break
        if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 0 and (data['name'] in case_list):

            # Remove case from case list to optimize later searches
            case_list = [x for x in case_list if x != data['name']]
            
            court_d = {}            
            case_year = data['decision_date'][0:4]
            w_count = len(data['casebody']['data']['opinions'][0]['text'].split())

            # Remove citations from opinion text
            
    
            # R-based calculations of readability
            try:
                r_read_mets = quanteda.textstat_readability(data['casebody']['data']['opinions'][0]['text'].replace('\n', ' '), measure = 'all')
                
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

                court_d.update(court = data['court']['name'], 
                               date = data['decision_date'], 
                               cite = data['citations'][0]['cite'], 
                               case = data['name'], 
                               year = case_year, 
                               word_count = w_count,
                               has_opinion = 1,
                               ARI_R = ari_r, RIX_R = rix_r,
                               Coleman_Liau_Grade_R = Coleman_Liau_Grade_R,
                               Coleman_Liau_Short_R = Coleman_Liau_Short_R,
                               Danielson_Bryan_R = Danielson_Bryan_R,
                               Dickes_Steiwer_R = Dickes_Steiwer_R,
                               ELF_R = ELF_R, 
                               Farr_Jenkins_Paterson_R = Farr_Jenkins_Paterson_R,
                               flesch_R = flesch_R, flesh_kincaid_R = flesh_kincaid_R,
                               FORCAST_R = FORCAST_R, Fucks_R = Fucks_R, 
                               FOG_R = FOG_R, Linsear_Write_R = Linsear_Write_R,
                               nWS_R = nWS_R, SMOG_R = SMOG_R, 
                               Strain_R = Strain_R,
                               Wheeler_Smith_R = Wheeler_Smith_R)
                rows_list.append(court_d)
                
                case_num += 1
                print(case_num)

            except:
                pass

scotus_df = pd.DataFrame(rows_list)
scotus_df.to_csv('benchmark_SCOTUS_readability_v2.csv', index = False)

