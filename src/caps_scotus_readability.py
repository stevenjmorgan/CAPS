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
#for i in range(12, 13): #len(files)
#    data1 = []
#    x = 0
#    findName = pd.DataFrame(columns = ['state_court'])
#    with open(files[i]) as f:
#        for line in f:
#            data1.append(json.loads(line))
#            s = pd.Series([data1[x]['court']['name']],
#                          index = ['state_court'])
#            findName = findName.append(s, ignore_index=True)
#            x += 1
#            if x == 1000:
#                break
#    print(findName.state_court.unique())

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
                   'Court of Appeals of Maryland'
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
for j in range(0, len(files)): #len(files)
    data = []
    with open(files[j]) as f:
        for line in f:
            data.append(json.loads(line))
    t1 = datetime.now()
    rows_list = []
    for i in range(0, len(data)):
        if (data[i]['court']['name'] in state_high_list) and len(data[i]['casebody']['data']['opinions']) > 0:
        
            court_d = {}
            num_scotus_cites = len(re.findall(scotus_pat, data[i]['casebody']['data']['opinions'][0]['text']))
            num_us_cites = len(re.findall(us_fed_pat, data[i]['casebody']['data']['opinions'][0]['text']))
            num_total_cites = len(re.findall(total_cites_pat, data[i]['casebody']['data']['opinions'][0]['text']))
            
            case_year = data[i]['decision_date'][0:4]
            case_decade = round_down(case_year)
            
            # Readability measures
            
            
            #len(scotus_pat.findall(data[i]['casebody']['data']['opinions'][0]['text']))
            #s = pd.Series([data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites],
            #              index = ['case','date','cite', 'court','SCOTUS_cites'])
            #state_court_d[states[j]] = state_court_d[states[j]].append(s, ignore_index=True)
            #state_court_d[states[j]].loc[i] = [data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites]
            
            court_d.update(court = data[i]['court']['name'], 
                           date = data[i]['decision_date'], 
                           cite = data[i]['citations'][0]['cite'], 
                           case = data[i]['name'], 
                           SCOTUS_cites = num_scotus_cites, 
                           year = case_year, decade = case_decade,
                           flesch = textstat.flesch_reading_ease(data[i]['casebody']['data']['opinions'][0]['text']),
                           flesch_kincaid = textstat.flesch_kincaid_grade(data[i]['casebody']['data']['opinions'][0]['text']),
                           gunning_fog = textstat.gunning_fog(data[i]['casebody']['data']['opinions'][0]['text']),
                           smog = textstat.smog_index(data[i]['casebody']['data']['opinions'][0]['text']),
                           ari = textstat.automated_readability_index(data[i]['casebody']['data']['opinions'][0]['text']),
                           coleman_liau = textstat.coleman_liau_index(data[i]['casebody']['data']['opinions'][0]['text']),
                           state = states[j].split('_data')[0].replace('_', ' ').capitalize(),
                           word_count = len(data[i]['casebody']['data']['opinions'][0]['text'].split()),
                           us_cites = num_us_cites,
                           total_cites = num_total_cites)
            rows_list.append(court_d)
            
    state_court_d[states[j]] = pd.DataFrame(rows_list)
    t2 = datetime.now()
    print(t2-t1)
     
with open('df_cites_readability_moreCites.pkl', 'wb') as handle:
    pickle.dump(state_court_d, handle, protocol=pickle.HIGHEST_PROTOCOL)
#state_court_d = pd.read_pickle('df_cites_readability_2_6.pkl')


# Convert dictionary of df's to single df, write to .csv
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df.to_csv('state_court_cases.csv', index = False)



exit()
#break


######### Group by decade ###########
# Test case to group by decade
state_court_d['alabama_data'].columns.values
test = state_court_d['alabama_data'].groupby(['decade']).mean()

# Create dictionary of dataframes for aggregated SCOTUS cites data
scotus_cites_decade= {}
scotus_columns = ['decade','SCOTUS_cites']
for i in range(0, len(state_court_d)):
    #scotus_cites_decade[name] = pd.DataFrame(columns=scotus_columns)
    try:
        scotus_cites_decade[states[i]] = state_court_d[states[i]].groupby(['decade']).mean()
        scotus_cites_decade[states[i]]['state'] = states[i].split('_data')[0].replace('_', ' ').capitalize()
    except:
        pass # Maryland has empty df, one other as well
        
states_decade_df = pd.concat(scotus_cites_decade.values(), ignore_index=False)
states_decade_df.reset_index(level=0, inplace=True)
states_decade_df.to_csv('state_decade.csv', index = False)


for i in range(0, len(state_court_d)):
    #scotus_cites_decade[name] = pd.DataFrame(columns=scotus_columns)
    try:
        state_court_d[states[i]]['state'] = states[i].split('_data')[0].replace('_', ' ').capitalize()
    except:
        pass # Maryland has empty df, one other as well

states_temp_df = pd.concat(state_court_d.values(), ignore_index=False)
states_temp_df.reset_index(level=0, inplace=True)
states_temp_df.to_csv('state_temp.csv', index=False)

# Group by decade by Average readability scores

sys.exit()


###############################################################################
### Plots -> Probably will just do in R (ggplot2)
###############################################################################
        
# Test alabama ggplot
test = scotus_cites_decade[states[0]]
test.reset_index(level=0, inplace=True)
p = ggplot(aes(x='decade', y='SCOTUS_cites'), data=test)
#p + geom_point() + geom_line()


decades =  test.index.tolist()[0::2]
state_names = []
for i in range(0, len(states)):
    state_names.append(states[i].split('_data')[0].capitalize())

title = str(state_names[0]) + ' High Court SCOTUS Citations'
test.plot(title=title, xticks = decades)


#pdf = matplotlib.backends.backend_pdf.PdfPages("scotus_cites.pdf")
for i in range(0, len(scotus_cites_decade)):
    try:
        title = str(state_names[i]) + ' High Court SCOTUS Citations'
        scotus_cites_decade[states[i]].plot(title=title, xticks = decades)
        fig_name = states[i] + '.png'
        plt.savefig(fig_name)
    except:
        pass
    
x = scotus_cites_decade[states[0]].plot(title=title, xticks = decades)

###############################################################################
# Extraneous code that may help if issues arise/de-bugging
###############################################################################

# Compare data for Alabama test case
#test_bama = state_court_d['alabama_data'] #72,218*5, 17:51 w/ append series approach: SAD!
#test_bama2 = state_court_d['alabama_data'] #72,218*5, 19:36 w/ .loc approach: SAD!
#test_bama3 = state_court_d['alabama_data'] #72,218*5, 0:08 w/ list of dict's approach: Wow!

### Alternate way of opening up .jsonl files -> slightly slower
#t1 = datetime.now()
#with open('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/alabama_data.jsonl') as f:
#    data2 = [json.loads(line) for line in f]
#t2 = datetime.now()
#print(t2-t1)
    
# List of state high courts
#state_courts_wiki = pd.read_html('https://en.wikipedia.org/wiki/State_supreme_court',
#                                 header = 0) #list of df's
#state_courts = state_courts_wiki[4] #single df
#state_courts = state_courts.iloc[:,0]
#state_high = state_courts.tolist()
#del(state_courts)
 
 # Play w/ dictionaries
#x = data[1]
#q = data[505]
#print(q['court']['name'])
#print(x['jurisdiction'])
#print(x['casebody']['data']['opinions'][0]['text'])
 
#y = data[2]
#print(y['casebody']['data']['opinions'][0]['text'])
 
# Create pandas dataframe for Alabama SC cases
#columns = ['case','cite', 'court']
#index = range(0, len(data))
#al_df = pd.DataFrame(index=index, columns=columns)
#al_df.head()
 
#print(al_df[0:1])
#print(al_df.at[0,'case'])
 
#df_.at[0,'case'] = np.nan
 
# Iterate through list of dictionaries
#for i in range(1, len(data)):
#    if data[i]['court']['name'] == 'Alabama Supreme Court':
#        al_df.at[i, 'court'] = data[i]['court']['name']
#        al_df.at[i, 'case'] = data[i]['name']
#        al_df.at[i, 'cite'] = data[i]['citations'][0]['cite']
         
#al_df[200:300]
#al_df.head()
 
# Append to dataframe
#t1 = datetime.now()
#scotus_pat = "\d{1,3}\sS\.Ct\.\s"
#num_scotus_cites = 0
#columns = ['court','date','cite','case','SCOTUS_cites']
#al_df = pd.DataFrame(index=[0], columns=columns)
#for i in range(1, len(data)):
#    if data[i]['court']['name'] == 'Alabama Supreme Court' and len(data[i]['casebody']['data']['opinions']) > 0:
#        num_scotus_cites = len(re.findall(scotus_pat, data[i]['casebody']['data']['opinions'][0]['text']))
#        #len(scotus_pat.findall(data[i]['casebody']['data']['opinions'][0]['text']))
#        s = pd.Series([data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites],
#                      index = ['case','date','cite', 'court','SCOTUS_cites'])
#        al_df = al_df.append(s, ignore_index=True)
#        #print(i)
#t2 = datetime.now()
#print(t2-t1)
 
# Remove first row (NaN's)
#al_df = al_df.iloc[1:]
 
#al_df.to_pickle('al_df_cites.pkl')
#al_df.to_csv('al_df_cites.csv')
#yo = pd.read_pickle('al_df_cites.pkl')
 
# For all 50 states
#d = {}
#states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
#          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
#          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
#          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
#          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
#for name in states:
#    d[name] = pd.DataFrame(columns=columns)

################# Test Case #############################
# Open alabama file as a test case
#data = []
#with open(files[0]) as f:
#    for line in f:
#        data.append(json.loads(line))
 
# Append to dataframe
#t1 = datetime.now()
#scotus_pat = "\d{1,3}\sS\.Ct\.\s"
#num_scotus_cites = 0
#for i in range(1, len(data)):
#    if data[i]['court']['name'] == 'Alabama Supreme Court' and len(data[i]['casebody']['data']['opinions']) > 0:
#        num_scotus_cites = len(re.findall(scotus_pat, data[i]['casebody']['data']['opinions'][0]['text']))
        #len(scotus_pat.findall(data[i]['casebody']['data']['opinions'][0]['text']))
#        s = pd.Series([data[i]['court']['name'],data[i]['name'],data[i]['decision_date'],data[i]['citations'][0]['cite'],num_scotus_cites],
#                      index = ['case','date','cite', 'court','SCOTUS_cites'])
#        state_court_d['alabama_data'] = state_court_d['alabama_data'] .append(s, ignore_index=True)
        #print(i)
#t2 = datetime.now()
#print(t2-t1)
#########################################################
        
#ny_courts = []
#data1 = []
#x = 0
#findName = pd.DataFrame(columns = ['state_court'])
#with open('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/new_york_data.jsonl') as f:
#    for line in f:
#        data1.append(json.loads(line))
#        ny_courts.append([data1[x]['court']['name']])
        #s = pd.Series([data1[x]['court']['name']],
        #              index = ['state_court'])
        #findName = findName.append(s, ignore_index=True)
#        x += 1
#            if x == 10000:
#                break
#print(list(set(ny_courts)))
 