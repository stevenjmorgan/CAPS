# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 14:22:29 2019

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
import nltk.data
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))

# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#sentences = sent_detector.tokenize(paragraph.strip())

#files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
files = list(glob.glob(os.path.join('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
#states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
states = [x.split('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
states = [x.replace("\\", "") for x in states]
states = [x.replace(".jsonl", "") for x in states]

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
                   'Maine Supreme Court', 'Supreme Court of Maine', 
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
columns = ['court','date','cite','case','SCOTUS_cites', 'year', 'decade', 
           'us_cites', 'fed_report', 'total_cites', 'pos_cites', 'neg_cites', 
           'state', 'cite_names']
for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)
    
# Loop through each file in dir, for each entry create pd.series, append to df
scotus_pat = "\d{1,3}\sS\.Ct\.\s"
us_fed_pat = "\d{1,3}\sU\.S\.\s"
fed_report_pat = '\d{1,3}\sF\.\dd\s\d{1,4}'
#total_cites_pat = '(\d+)\s(.+?)\s(\d+)'
total_cites_pat = '(\d{1,3})\s(.{2,12})\s(\d+)'

'''Using re.compile() and saving the resulting regular expression object for reuse
 is more efficient when the expression will be used several times in a single program.
'''

num_scotus_cites = 0
case_year = ''
case_decade = 0
#pos_cite = 0
#neg_cite = 0
analyzer = SentimentIntensityAnalyzer()
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
            #num_total_cites = len(re.findall(total_cites_pat, data[i]['casebody']['data']['opinions'][0]['text']))
            fed_report = len(re.findall(fed_report_pat, data[i]['casebody']['data']['opinions'][0]['text']))
            
            
            
            cites = re.findall(total_cites_pat, data[i]['casebody']['data']['opinions'][0]['text'])
            num_total_cites = len(cites)
            
            
            case_cites = []
            for match in cites:
                case_cites.append(match)
                #print(match)
            
            case_year = data[i]['decision_date'][0:4]
            case_decade = round_down(case_year)
            
            pos_cite = 0
            neg_cite = 0
            
            # Measuring pos. and neg. citations
            sentences = sent_detector.tokenize(data[i]['casebody']['data']['opinions'][0]['text'].strip())
            
            for index, line in enumerate(sentences):
                if re.search(total_cites_pat, line):
                    #print(sentences[index-1])
                    sentiment = analyzer.polarity_scores(sentences[index-1])
                    #print(sentiment)
                    if sentiment['compound'] > 0.05:
                        pos_cite += 1
                    if sentiment['compound'] > -0.05:
                        neg_cite += 1

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
                           ###### = data[i]['casebody']['data']['opinions'][0]['text'],
                           us_cites = num_us_cites,
                           total_cites = num_total_cites,
                           pos_cites = pos_cite,
                           neg_cites = neg_cite,
                           state = states[j].split('_data')[0].replace('_', ' ').capitalize(),
                           cite_names = case_cites)
            rows_list.append(court_d)
            
    state_court_d[states[j]] = pd.DataFrame(rows_list)
    t2 = datetime.now()
    print(t2-t1)
    print('Finished: ' + str(states[j]))
     
with open('df_pos_cites.pkl', 'wb') as handle:
    pickle.dump(state_court_d, handle, protocol=pickle.HIGHEST_PROTOCOL)
#state_court_d = pd.read_pickle('df_cites_readability_2_6.pkl')


# Convert dictionary of df's to single df, write to .csv
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df.to_csv('state_court_pos_cites.csv', index = False)


exit()

# Test sentence parser
scotus_pat = "\d{1,3}\sS\.Ct\.\s"
us_fed_pat = "\d{1,3}\sU\.S\.\s"
#total_cites_pat = '(\d+)\s(.+?)\s(\d+)'

test = data[122027]['casebody']['data']['opinions'][0]['text']
test

sentences = sent_detector.tokenize(test.strip())

scotus_pat = "\d{1,3}\sS\.Ct\.\s"
total_cites_pat = '(\d{1,3})\s(.{2,6})\s(\d+)'
analyzer = SentimentIntensityAnalyzer()
analyzer.polarity_scores()

pos_cite = 0
neg_cite = 0

'''positive sentiment: compound score >= 0.5
neutral sentiment: (compound score > -0.5) and (compound score < 0.5)
negative sentiment: compound score <= -0.5
'''

for index, line in enumerate(sentences):
    if re.search(total_cites_pat, line):
        #print(sentences[index-1])
        sentiment = analyzer.polarity_scores(sentences[index-1])
        print(sentiment)
        if sentiment['compound'] > 0.05:
            pos_cite += 1
        if sentiment['compound'] > -0.05:
            neg_cite += 1


print(pos_cite, neg_cite)
#analyzer.polarity_scores(sentences[10])
    
exit()
