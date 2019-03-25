# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:18:41 2019

@author: steve
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script reads in 52 state high court opinion text data from the CAPS 
project and extracts SCOTUS citations and readability measures.
This code is written in Python3.

user: steven morgan
date: Jan. 31, 2019
"""

import spacy
from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work
from datetime import datetime
import json
#import numpy as np 
import pandas as pd
import numpy as np
import re
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
import lexnlp.extract.en.citations
import lexnlp.nlp.en.segments.sentences
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
#with open('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/alabama_data.jsonl') as f:
#with open('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/alabama_data.jsonl') as f:
#    for line in f:
#        data.append(json.loads(line))
#t2 = datetime.now()
#print(t2-t1)

#files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
files = list(glob.glob(os.path.join('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
#states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
states = [x.split('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
states = [x.replace("\\", "") for x in states]
states = [x.replace(".jsonl", "") for x in states]
 
### Determine what CAPS says state court name is...runs for a while
# =============================================================================
# for i in range(19, 20): #len(files)
#     data1 = []
#     x = 0
#     findName = pd.DataFrame(columns = ['state_court'])
#     with open(files[i]) as f:
#         for line in f:
#             data1.append(json.loads(line))
#             s = pd.Series([data1[x]['court']['name']],
#                           index = ['state_court'])
#             findName = findName.append(s, ignore_index=True)
#             x += 1
#             if x == 1000:
#                 break
#     print(findName.state_court.unique())
#     
# # Faster
# courts = []
# x = 0
# with open(files[19]) as f:
#     #for line in f:
#     #    data.append(json.loads(line))
#     #court_d = {}
#     for line in f:
#         data = json.loads(line)
#         courts.append(data['court']['name'])
#         if data['court']['name'] == 'Court of Appeals of Maryland':
#             x += 1
# courts_uni = list(set(courts))
# print(x)
# =============================================================================


### look at kentucky and maine again
# Hard code state high courts to match .jsonl files (names change over time)
state_high_list = ['Alabama Supreme Court','Alaska Supreme Court', 
                   'Alaska Supreme Court Alaska', 'Arizona Supreme Court',
                   'Arkansas Supreme Court', 
                   'Court Abbreviations Arkansas Supreme Court',
                   'Supreme Court of California', 'Colorado Supreme Court',
                   'Connecticut Supreme Court', 
                   'Connecticut Supreme Court of Errors', 
                   'Delaware Supreme Court', 
                   'Delaware Court of Errors and Appeals', 
                   'Florida Supreme Court', 'Supreme Court of Florida',
                   'Supreme Court of Georgia',  
                   'Supreme Court of the State of Hawaii', 
                   'Supreme Court of the Territory of Hawaii',
                   'Supreme Court of the Republic of Hawaii',
                   'Illinois Supreme Court',
                   'Idaho Supreme Court', 'Supreme Court of Indiana',
                   'Supreme Court of Indianad', 'Iowa Supreme Court',
                   'Kansas Supreme Court', 'Louisiana Supreme Court',
                   'Supreme Court of Kentucky',
                   'Maine Supreme Judicial Court', 
                   'Court of Appeals of Maryland',
                   'High Court of Chancery of Maryland', 
                   'Massachusetts Supreme Judicial Court', 
                   'Michigan Supreme Court', 'Supreme Court of Michigan',
                   'Minnesota Supreme Court', 'Mississippi Supreme Court',
                   'High Court of Errors and Appeals of Mississippi',
                   'Supreme Court of Missouri', 'Montana Supreme Court',
                   'Nebraska Supreme Court', 'Supreme Court of Nevada',
                   'New Hampshire Supreme Court', 
                   'New Hampshire Committee of the Privy Council', 
                   'New Jersey Supreme Court', 
                   'New Jersey Court of Errors and Appeals',
                   'Supreme Court of New Mexico', 
                   'Supreme Court of North Carolina', 
                   'Ney York Court for the Correction of Errors',
                   'New York Court of Appeal', 'New York Court of Errors',
                   'New York Court of Appeals',
                   'Court of Errors of the State of New York',
                   'Court of Chancery',
                   'North Dakota Supreme Court', 'Supreme Court of Ohio',
                   'Oklahoma Supreme Court',
                   'Oklahoma Court of Criminal Appeals',
                   'Oregon Supreme Court', 
                   'Pennsylvania Supreme Court', 
                   'Supreme Court of Pennsylvania',
                   'Supreme Court of Rhode Island',
                   'Rhode Island Supreme Court', 
                   'Supreme Court of South Carolina', 
                   'Constitutional Court of South Carolina',
                   'South Carolina Court of Errors', 
                   'South Carolina Supreme Court', 'Tennessee Supreme Court',
                   'Supreme Court of Errors and Appeals of Tennessee',
                   'Utah Supreme Court', 'Vermont Supreme Court',
                   'Supreme Court of Appeals of Virginia',
                   'Supreme Court of Virginia',
                   'High Court of Chancery of Virginia',
                   'Washington Supreme Court', 
                   'Supreme Court of Appeals of West Virginia',
                   'Wisconsin Supreme Court', 'Supreme Court of Wyoming']

### Read in data into list of dictionaries
# Create dictionary of dataframes for each file
state_court_d = {}
state_court_d_wide = {}
columns = ['case_id', 'court','date','cite','case','year', 'decade', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'number_cites', 'citations',
           'pos_cites', 'neg_cites', 'has_opinion', 'total_opins', 'greater50',
           'opin_author', 'judges']
for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)
    state_court_d_wide[name] = pd.DataFrame(columns=columns)


# Loop through each file in dir, for each entry create pd.series, append to df
#scotus_pat = "\d{1,3}\sS\.Ct\.\s"
#us_fed_pat = "\d{1,3}\sU\.S\.\s"
#total_cites_pat = '(\d+)\s(.+?)\s(\d+)'
#num_scotus_cites = 0
case_year = ''
case_decade = 0
case_id = 0
analyzer = SentimentIntensityAnalyzer() # Vader sentiment analysis
for j in range(0, len(files)): #len(files)
    
    rows_list = []
    t1 = datetime.now()
    
    with open(files[j]) as f:
        #for line in f:
        #    data.append(json.loads(line))
        court_d = {}
        for line in f:
        
            #if case_id == 100:
            #    break
            
            data = json.loads(line)
            
            if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 0: #and len(data['casebody']['data']['opinions'][0]['text'].split()) > 50:
                
                court_d = {}
                
                # Store case year and decade
                case_year = data['decision_date'][0:4]
                case_decade = round_down(case_year)
                
                # Remove citations, calculate readability
                text_clean = data['casebody']['data']['opinions'][0]['text'].replace('(\d+)\s(.+?)\s(\d+)', '')
                flesch = textstat.flesch_reading_ease(text_clean)
                flesch_kincaid = textstat.flesch_kincaid_grade(text_clean)
                fog = textstat.gunning_fog(text_clean)
                smog = textstat.smog_index(text_clean)
                ari = textstat.automated_readability_index(text_clean)
                coleman_liau = textstat.coleman_liau_index(text_clean)
                
                # Count words, published opinions, extract state
                w_count = len(data['casebody']['data']['opinions'][0]['text'].split())
                total_opins = len(data['casebody']['data']['opinions'])
                state = states[j].split('_data')[0].replace('_', ' ').capitalize()
                greater50 = 1 if w_count > 50 else 0
                
                # Extract citations in generator object, store in list
                cite_gen = lexnlp.extract.en.citations.get_citations(data['casebody']['data']['opinions'][0]['text'], return_source=True, as_dict=True)
                cite_list = list(cite_gen)
                
                # Count # of citations
                gen_count = len(cite_list)
                cite_names = ''
                
                # Opinion author
                try:
                    opin_author = data['casebody']['data']['opinions'][0]['author']
                except:
                    opin_author = ''
                    pass
                
                # Judges
                try:
                    #judges = str(data['casebody']['data']['judges'])
                    judges = ''.join(data['casebody']['data']['judges'])
                except:
                    judges = ''
                    pass
                
                # Create regex's based on extracted citations
                for el in range(0, len(cite_list)):
                    if el == 0:
                        cite_names = cite_list[el]['citation_str']
                    else:
                        cite_names = cite_names + ', ' + cite_list[el]['citation_str']
                        
                # Create list of citation names, Make a regex that matches if any of our regexes match.
                cite_list_source = [d['citation_str'] for d in cite_list]
                cite_list_source = [e.replace('(', '').replace(')', '') for e in cite_list_source]
                cite_list_source = list(set(cite_list_source))
                cite_list_source = [a for a in cite_list_source if len(a.split()) < 7]
                try:
                    cite_list_regex = [re.compile(elem) for elem in cite_list_source]
                except:
                    pass
                
                # Sentence parser
                sentences = lexnlp.nlp.en.segments.sentences.get_sentence_list(data['casebody']['data']['opinions'][0]['text'].strip())
                 
                pos_cite = 0
                neg_cite = 0
                
                for index, line in enumerate(sentences):
                    if any(regex.match(line) for regex in cite_list_regex):
                        #print(sentences[index-1])
                        sentiment = analyzer.polarity_scores(sentences[index-1])
                        #print(sentiment)
                        if sentiment['compound'] > 0.05:
                            pos_cite += 1
                        if sentiment['compound'] > -0.05:
                            neg_cite += 1
                
                if gen_count > 0:
                
                    # Create row for each citation
                    for el in cite_list:
                        
                        court_d = {}
                        
                        cite_names = el['citation_str']
                        reporter = el['reporter_full_name']
                    
                        court_d.update(case_id = case_id,
                                       court = data['court']['name'], 
                                       date = data['decision_date'], 
                                       cite = data['citations'][0]['cite'], 
                                       case = data['name'], 
                                       ###SCOTUS_cites = num_scotus_cites, 
                                       year = case_year, decade = case_decade,
                                       citations = cite_names,
                                       reporter = reporter,
                                       number_cites = gen_count,
                                       pos_cites = pos_cite, neg_cites = neg_cite,
                                       flesch = flesch,
                                       flesch_kincaid = flesch_kincaid,
                                       gunning_fog = fog,
                                       smog = smog,
                                       ari = ari,
                                       coleman_liau = coleman_liau,
                                       state = state,
                                       word_count = w_count,
                                       has_opinion = 1,
                                       total_opins = total_opins,
                                       greater50 = greater50,
                                       opin_author = opin_author,
                                       judges = judges)
                        rows_list.append(court_d)
                        
                else:
                    
                    court_d = {}
                    
                    court_d.update(case_id = case_id,
                                   court = data['court']['name'], 
                                   date = data['decision_date'], 
                                   cite = data['citations'][0]['cite'], 
                                   case = data['name'], 
                                   ###SCOTUS_cites = num_scotus_cites, 
                                   year = case_year, decade = case_decade,
                                   #citations = cite_names,
                                   #reporter = reporter,
                                   number_cites = gen_count,
                                   flesch = flesch,
                                   flesch_kincaid = flesch_kincaid,
                                   gunning_fog = fog,
                                   smog = smog,
                                   ari = ari,
                                   coleman_liau = coleman_liau,
                                   state = state,
                                   word_count = w_count,
                                   has_opinion = 1,
                                   total_opins = total_opins,
                                   greater50 = greater50,
                                   opin_author = opin_author,
                                   judges = judges)
                    rows_list.append(court_d)
                
                case_id += 1
             
        if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) == 0:
                
            court_d = {}
            
            case_year = data['decision_date'][0:4]
            case_decade = round_down(case_year)
        
            court_d.update(case_id = case_id,
                           court = data['court']['name'], 
                           date = data['decision_date'], 
                           cite = data['citations'][0]['cite'], 
                           case = data['name'], 
                           year = case_year, decade = case_decade,
                           state = state,
                           has_opinion = 0)
            rows_list.append(court_d)
                
            case_id += 1
            
            
        state_court_d[states[j]] = pd.DataFrame(rows_list)
        state_court_d[states[j]] = state_court_d[states[j]][columns] # Rearrange columns
        
        state_court_d_wide[states[j]] = state_court_d[states[j]].fillna(-999).groupby(['case_id', 'court','date','cite','case','year', 'decade', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'pos_cites', 'neg_cites', #'number_cites', 
           'has_opinion', 'total_opins', 'greater50', 'opin_author', 'judges'], as_index=False).mean() #opin_author, judges
        #state_court_d_wide[states[j]] = state_court_d_wide[states[j]][columns]
        
        state_court_d_wide[states[j]] = state_court_d_wide[states[j]].replace(-999, np.NaN)
        
        t2 = datetime.now()
        print(state + ': ' + str(t2-t1))


# Dimension check: (62235, 10)
#state_court_d[states[0]].shape
#state_court_d[states[0]].head(100).to_csv('sample.csv', index = False)
#state_court_d['alabama_data']['citations'][1000:1003]
#state_court_d['alabama_data']['number_cites'][1000:1003]
#state_court_d['alabama_data']['citations'][1001]


with open('df_long_final3-25.pkl', 'wb') as handle:
    pickle.dump(state_court_d, handle, protocol=pickle.HIGHEST_PROTOCOL)
#state_court_d = pd.read_pickle('df_long_final.pkl')

# Convert dictionary of df's to single df, write to .csv (long: one case-citation per line)
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df.to_csv('state_court_long_final3-25.csv', index = False)

# Convert from wide to long (one case per row)
states_single_df_wide = pd.concat(state_court_d_wide.values(), ignore_index=True, sort=False)
#states_single_df_wide = states_single_df.groupby(['case_id', 'court','date','cite','case','year', 'decade', 
#           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
#           'coleman_liau', 'state', 'word_count', 'pos_cites', 'neg_cites', #'number_cites', 
#           'has_opinion', 'total_opins', 'greater50', 'opin_author', 'judges']).mean()
with open('df_wide_final3-25.pkl', 'wb') as handle:
    pickle.dump(states_single_df_wide, handle, protocol=pickle.HIGHEST_PROTOCOL)
states_single_df_wide.to_csv('state_court_wide_final3-25.csv', index = False)


exit()