#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script reads in SCOTUS opinion text data from the CAPS 
project and extracts SCOTUS citations and readability measures.
This code is written in Python3.
Created on Thu Feb 14 09:12:14 2019

@author: sum410
"""

import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work
from datetime import datetime
import json
#import numpy as np 
import pandas as pd
import re
import os
import glob
import sys
import pickle
#from ggplot import aes
#from ggplot import ggplot
#import matplotlib.pyplot as plt
import textstat
#import matplotlib.backends.backend_pdf
#import timeit

# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))

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
def avg_syllables_per_word(text): 
    syllable = syllables_count(text) 
    words = word_count(text) 
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
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')
 
###############################################################################
# Read in data into list first (inconsistent graph structure in .jsonl files)
#t1 = datetime.now()
#data = []
#with open('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/alabama_data.jsonl') as f:
#with open('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/alabama_data.jsonl') as f:
#    for line in f:
#        data.append(json.loads(line))
#t2 = datetime.now()
#print(t2-t1)

#files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/','*.*')))
files = list(glob.glob(os.path.join('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/','*.*')))
#states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.split('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.replace("\\", "") for x in states]
states = [x.replace(".jsonl", "") for x in states]
 
### Determine what CAPS says state court name is...runs for a while
# =============================================================================
# court_list = []
# t1 = datetime.now()
# with open(files[0]) as f:
#     for line in f:
#         #print(type(line))
#         #print(line)
#         #break
#     
#         data = json.loads(line)
#         if len(data['court']['name']) > 0:
#             court_list.append(data['court']['name'])
# uni_courts = list(set(court_list))
# with open('scotus_court_names.txt', 'w') as f:
#     for item in uni_courts:
#         f.write("%s\n" % item)
# =============================================================================


### look at kentucky and maine again
# Hard code state high courts to match .jsonl files (names change over time)
state_high_list = ['United States Supreme Court', 
                   'Supreme Court of United States',
                   'United State Supreme Court',
                   'Supreme Court of the United States']

### Read in data into list of dictionaries
# Create dictionary of dataframes for each file
state_court_d = {}
columns = ['court','date','cite','case','SCOTUS_cites', 'year', 'decade', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'us_cites', 'total_cites']
for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)

# Loop through each file in dir, for each entry create pd.series, append to df
scotus_pat = "\d{1,3}\sS\.Ct\.\s"
us_fed_pat = "\d{1,3}\sU\.S\.\s"
total_cites_pat = '(\d+)\s(.+?)\s(\d+)'
num_scotus_cites = 0
case_year = ''
case_decade = 0
x = 0

#data = []
rows_list = []
t1 = datetime.now()
with open(files[0]) as f:
    for line in f:
        #print(type(line))
        #print(line)
        #break
    
        data = json.loads(line)
        
        if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 0:
        
            print("SCOTUS CASE")
            court_d = {}
            num_scotus_cites = len(re.findall(scotus_pat, data['casebody']['data']['opinions'][0]['text']))
            num_us_cites = len(re.findall(us_fed_pat, data['casebody']['data']['opinions'][0]['text']))
            num_total_cites = len(re.findall(total_cites_pat, data['casebody']['data']['opinions'][0]['text']))
            
            case_year = data['decision_date'][0:4]
            case_decade = round_down(case_year)
            
            # Readability measures
            
            
            #len(scotus_pat.findall(data[i]['casebody']['data']['opinions'][0]['text']))
            #s = pd.Series([data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites],
            #              index = ['case','date','cite', 'court','SCOTUS_cites'])
            #state_court_d[states[j]] = state_court_d[states[j]].append(s, ignore_index=True)
            #state_court_d[states[j]].loc[i] = [data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites]
            
            court_d.update(court = data['court']['name'], 
                           date = data['decision_date'], 
                           cite = data['citations'][0]['cite'], 
                           case = data['name'], 
                           SCOTUS_cites = num_scotus_cites, 
                           year = case_year, decade = case_decade,
                           flesch = textstat.flesch_reading_ease(data['casebody']['data']['opinions'][0]['text']),
                           flesch_kincaid = textstat.flesch_kincaid_grade(data['casebody']['data']['opinions'][0]['text']),
                           gunning_fog = textstat.gunning_fog(data['casebody']['data']['opinions'][0]['text']),
                           smog = textstat.smog_index(data['casebody']['data']['opinions'][0]['text']),
                           ari = textstat.automated_readability_index(data['casebody']['data']['opinions'][0]['text']),
                           coleman_liau = textstat.coleman_liau_index(data['casebody']['data']['opinions'][0]['text']),
                           #state = states[j].split('_data')[0].replace('_', ' ').capitalize(),
                           word_count = len(data['casebody']['data']['opinions'][0]['text'].split()),
                           us_cites = num_us_cites,
                           total_cites = num_total_cites)
            rows_list.append(court_d)
            #sys.exit()
            #print(line)
            #break
            
t2 = datetime.now()
print(t2-t1)
state_court_d[states[0]] = pd.DataFrame(rows_list)

        
    
#data.append(json.loads(line))




# =============================================================================
# for j in range(0, len(files)): #len(files)
#     data = []
#     t1 = datetime.now()
#     with open(files[j]) as f:
#         for line in f:
#             data.append(json.loads(line))
#             x += 1
#             if x == 2:
#                 break
#     t2 = datetime.now()
#     print(t2-t1)
#     
#     t1 = datetime.now()
#     rows_list = []
#     for i in range(0, len(data)):
#         if (data[i]['court']['name'] in state_high_list) and len(data[i]['casebody']['data']['opinions']) > 0:
#         
#             court_d = {}
#             num_scotus_cites = len(re.findall(scotus_pat, data[i]['casebody']['data']['opinions'][0]['text']))
#             num_us_cites = len(re.findall(us_fed_pat, data[i]['casebody']['data']['opinions'][0]['text']))
#             num_total_cites = len(re.findall(total_cites_pat, data[i]['casebody']['data']['opinions'][0]['text']))
#             
#             case_year = data[i]['decision_date'][0:4]
#             case_decade = round_down(case_year)
#             
#             # Readability measures
#             
#             
#             #len(scotus_pat.findall(data[i]['casebody']['data']['opinions'][0]['text']))
#             #s = pd.Series([data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites],
#             #              index = ['case','date','cite', 'court','SCOTUS_cites'])
#             #state_court_d[states[j]] = state_court_d[states[j]].append(s, ignore_index=True)
#             #state_court_d[states[j]].loc[i] = [data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites]
#             
#             court_d.update(court = data[i]['court']['name'], 
#                            date = data[i]['decision_date'], 
#                            cite = data[i]['citations'][0]['cite'], 
#                            case = data[i]['name'], 
#                            SCOTUS_cites = num_scotus_cites, 
#                            year = case_year, decade = case_decade,
#                            flesch = textstat.flesch_reading_ease(data[i]['casebody']['data']['opinions'][0]['text']),
#                            flesch_kincaid = textstat.flesch_kincaid_grade(data[i]['casebody']['data']['opinions'][0]['text']),
#                            gunning_fog = textstat.gunning_fog(data[i]['casebody']['data']['opinions'][0]['text']),
#                            smog = textstat.smog_index(data[i]['casebody']['data']['opinions'][0]['text']),
#                            ari = textstat.automated_readability_index(data[i]['casebody']['data']['opinions'][0]['text']),
#                            coleman_liau = textstat.coleman_liau_index(data[i]['casebody']['data']['opinions'][0]['text']),
#                            state = states[j].split('_data')[0].replace('_', ' ').capitalize(),
#                            word_count = len(data[i]['casebody']['data']['opinions'][0]['text'].split()),
#                            us_cites = num_us_cites,
#                            total_cites = num_total_cites)
#             rows_list.append(court_d)
#             
#     state_court_d[states[j]] = pd.DataFrame(rows_list)
#     t2 = datetime.now()
#     print(t2-t1)
# =============================================================================
     
with open('df_cites_readability_SCOTUS.pkl', 'wb') as handle:
    pickle.dump(state_court_d, handle, protocol=pickle.HIGHEST_PROTOCOL)
#state_court_d = pd.read_pickle('df_cites_readability_2_6.pkl')


# Convert dictionary of df's to single df, write to .csv
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df.to_csv('scotus_cases.csv', index = False)



sys.exit()
