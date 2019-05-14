# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:44:44 2019

@author: sum410
"""

import os, warnings, gensim, nltk, multiprocessing, glob, json, pickle
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from ds_voc.text_processing import TextProcessing

# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))

# Set working directory
#os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

warnings.filterwarnings(action = 'ignore')

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
                   'Supreme Court of New Jersey',
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
                   'Texas Supreme Court', 'Texas Courts of Appeals',
                   'Texas Court of Appeals', 'South Dakota Supreme Court',
                   'Supreme Court of Errors and Appeals of Tennessee',
                   'Utah Supreme Court', 'Vermont Supreme Court',
                   'Supreme Court of Appeals of Virginia',
                   'Supreme Court of Virginia',
                   'High Court of Chancery of Virginia',
                   'Washington Supreme Court', 
                   'Supreme Court of Appeals of West Virginia',
                   'Wisconsin Supreme Court', 'Supreme Court of Wyoming']

state_court_d = {}
state_court_d_wide = {}
columns = ['case_id', 'court','date','cite','case','year', 'decade', 'text']

for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)
    state_court_d_wide[name] = pd.DataFrame(columns=columns)

stop_re = '\\b'+'\\b|\\b'.join(nltk.corpus.stopwords.words('english'))+'\\b'

# Loop through each .jsonl, store in df    
case_year = ''
case_decade = 0
case_id = 0
for j in range(0, len(files)): #0, len(files)
    
    rows_list = []
    #t1 = datetime.now()
    
    
    with open(files[j]) as f:
        #for line in f:
        #    data.append(json.loads(line))
        court_d = {}
        for line in f:
        
            #if case_id == 10:
            #    break
            
            data = json.loads(line)
            
            if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 0: #and len(data['casebody']['data']['opinions'][0]['text'].split()) > 50:
                
                court_d = {}
                
                # Store case year and decade
                case_year = data['decision_date'][0:4]
                case_decade = round_down(case_year)
                state = states[j].split('_data')[0].replace('_', ' ').capitalize()
                
                
                court_d = {}
                
                court_d.update(case_id = case_id,
                               court = data['court']['name'], 
                               date = data['decision_date'], 
                               cite = data['citations'][0]['cite'], 
                               case = data['name'], 
                               year = case_year, decade = case_decade,
                               text = data['casebody']['data']['opinions'][0]['text'].replace('[^a-zA-Z]',' ').lower().replace(stop_re, ''))
                rows_list.append(court_d)
                
                case_id += 1
                
        state_court_d[states[j]] = pd.DataFrame(rows_list)
        print(state + ' done')

# Convert dictionary of df's to single df, write to .csv (long: one case-citation per line)
states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
state_opins_text = states_single_df

#state_opins_text.to_csv('state_court_text.csv', index = False)
#with open('state_opins_text.pkl', 'wb') as handle:
#    pickle.dump(state_opins_text, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Split df into 5 parts, save each
#df_list = np.array_split(state_opins_text, 5)
#df_list[0].to_pickle('state_opins_text1.pkl')
#df_list[1].to_pickle('state_opins_text2.pkl')
#df_list[2].to_pickle('state_opins_text3.pkl')
#df_list[3].to_pickle('state_opins_text4.pkl')
#df_list[4].to_pickle('state_opins_text5.pkl')

### Load in each pickle file and concatenate
###

### Process text
#state_opins_text['text.clean'] = state_opins_text['text'].str.replace('[^a-zA-Z]',' ').str.lower()
#stop_re = '\\b'+'\\b|\\b'.join(nltk.corpus.stopwords.words('english'))+'\\b'
#state_opins_text['text.clean'] = state_opins_text['text.clean'].str.replace(stop_re, '')



raw = list(state_opins_text['text'])
print(len(raw))


# word2vec expects a list of list: each document is a list of tokens
te = TextProcessing()
sentences = [te.stop_and_stem(c) for c in cleaned]


  
# Create CBOW model 
model1 = gensim.models.Word2Vec(data, min_count = 100,  
                              size = 300, window = 5) 

# Detect common phrases so that we may treat each one as its own word
phrases = gensim.models.phrases.Phrases(state_opins_text['text'].tolist())
phraser = gensim.models.phrases.Phraser(phrases)
train_phrased = phraser[state_opins_text['text'].tolist()]

multiprocessing.cpu_count()

# Run w2v w/ default parameters
w2v = gensim.models.word2vec.Word2Vec(sentences=train_phrased,workers=12)
w2v.save('w2v_v1')