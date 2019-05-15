# -*- coding: utf-8 -*-
"""
Created on Sat May 11 13:58:14 2019

@author: steve
"""

import pandas as pd
import re
import os
import glob
import json
import textstat
from textstat.textstat import textstatistics, easy_word_set, legacy_round #pip install; conda install will not work


# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))

# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

#files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/','*.*')))
files = list(glob.glob(os.path.join('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data/','*.*')))
#states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.split('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/SCOTUS_Data')[1] for x in files]
states = [x.replace("\\", "") for x in states]
states = [x.replace(".jsonl", "") for x in states]

state_high_list = ['United States Supreme Court', 
                   'Supreme Court of United States',
                   'United State Supreme Court',
                   'Supreme Court of the United States']

### Read in data into list of dictionaries
# Create dictionary of dataframes for each file
state_court_d = {}
columns = ['court','date','cite','case','SCOTUS_cites', 'year', 'decade', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'us_cites', 'total_cites',
           'opin_text']
for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)
    
num_scotus_cites = 0
case_year = ''
case_decade = 0

rows_list = []
with open(files[0]) as f:
    for line in f:
        
        data = json.loads(line)
        
        if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 0:
        
            #print("SCOTUS CASE")
            court_d = {}
            #num_scotus_cites = len(re.findall(scotus_pat, data['casebody']['data']['opinions'][0]['text']))
            #num_us_cites = len(re.findall(us_fed_pat, data['casebody']['data']['opinions'][0]['text']))
            #num_total_cites = len(re.findall(total_cites_pat, data['casebody']['data']['opinions'][0]['text']))
            
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
                           #flesch = textstat.flesch_reading_ease(data['casebody']['data']['opinions'][0]['text']),
                           #flesch_kincaid = textstat.flesch_kincaid_grade(data['casebody']['data']['opinions'][0]['text']),
                           #gunning_fog = textstat.gunning_fog(data['casebody']['data']['opinions'][0]['text']),
                           #smog = textstat.smog_index(data['casebody']['data']['opinions'][0]['text']),
                           #ari = textstat.automated_readability_index(data['casebody']['data']['opinions'][0]['text']),
                           #coleman_liau = textstat.coleman_liau_index(data['casebody']['data']['opinions'][0]['text']),
                           #state = states[j].split('_data')[0].replace('_', ' ').capitalize(),
                           word_count = len(data['casebody']['data']['opinions'][0]['text'].split()),
                           opin_text = data['casebody']['data']['opinions'][0]['text'])#,
                           #us_cites = num_us_cites,
                           #total_cites = num_total_cites)
            rows_list.append(court_d)
            #sys.exit()
            #print(line)
            #break
            
state_court_d[states[0]] = pd.DataFrame(rows_list)
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df['year_num'] = pd.to_numeric(states_single_df['year'])
states_single_df['year_num'].describe()
scotus_rep = states_single_df.loc[(states_single_df['year_num'] >= 1953) & (states_single_df['year_num'] <= 2007)] #& (states_single_df['word_count'] > 799)]
#scotus_rep = states_single_df.loc[(states_single_df['year_num'] >= 1953) & (states_single_df['year_num'] <= 2007)]
#scotus = scotus_rep.drop_duplicates()
scotus_rep = scotus_rep.sort_values(by=['year_num'])


scotus_rep.to_csv('scotus_rep.csv', index = False)

