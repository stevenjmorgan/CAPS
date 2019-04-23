# -*- coding: utf-8 -*-
"""
Created on Mon Apr 7 18:27:45 2019

@author: steve
"""

import os, glob, json, lexnlp.extract.en.citations, lexnlp.nlp.en.segments.sentences, textstat, re, pickle
import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Round year down to decade
def round_down(num):
    return str(int(num) - (int(num)%10))


# Set working directory
os.chdir('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/')
#os.chdir('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/')

files = list(glob.glob(os.path.join('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
#files = list(glob.glob(os.path.join('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data/','*.*')))
states = [x.split('C:/Users/steve/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
#states = [x.split('C:/Users/sum410/Dropbox/PSU2018-2019/RA/CAP/Bulk_Data')[1] for x in files]
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

### Read in data into list of dictionaries
# Create dictionary of dataframes for each file
state_court_d = {}
state_court_d_wide = {}
columns = ['case_id', 'court','date','cite','case','year', 'decade', 
           'flesch', 'flesch_kincaid', 'gunning_fog', 'smog', 'ari', 
           'coleman_liau', 'state', 'word_count', 'number_cites', #'citations',
           'pos_cites', 'neg_cites', 'total_opins', 'greater50', 'opin_author',
           'judges', 'opin_type']
for name in states:
    state_court_d[name] = pd.DataFrame(columns=columns)
    state_court_d_wide[name] = pd.DataFrame(columns=columns)

# Loop through each file in dir, for each entry create pd.series, append to df
case_year = ''
case_decade = 0
case_id = 0
analyzer = SentimentIntensityAnalyzer() # Vader sentiment analysis
for j in range(0, len(files)): #0, len(files)
    
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
            
            if (data['court']['name'] in state_high_list) and len(data['casebody']['data']['opinions']) > 1:
                
                # Store case year and decade
                case_year = data['decision_date'][0:4]
                case_decade = round_down(case_year)
                
                total_opins = len(data['casebody']['data']['opinions'])
                
                # Judges
                try:
                    #judges = str(data['casebody']['data']['judges'])
                    judges = ''.join(data['casebody']['data']['judges'])
                except:
                    judges = ''
                    pass
                
                for opin in range(0, len(data['casebody']['data']['opinions'])):
                    
                    if data['casebody']['data']['opinions'][opin]['type'] == 'majority':
                        #print('This should pass...')
                        pass
                    
                    else:
                    
                        court_d = {}
                        
                        # Remove citations, calculate readability
                        text_clean = data['casebody']['data']['opinions'][opin]['text'].replace('(\d+)\s(.+?)\s(\d+)', '')
                        flesch = textstat.flesch_reading_ease(text_clean)
                        flesch_kincaid = textstat.flesch_kincaid_grade(text_clean)
                        fog = textstat.gunning_fog(text_clean)
                        smog = textstat.smog_index(text_clean)
                        ari = textstat.automated_readability_index(text_clean)
                        coleman_liau = textstat.coleman_liau_index(text_clean)
                        
                        # Count words, published opinions, extract state
                        w_count = len(data['casebody']['data']['opinions'][opin]['text'].split())
                        state = states[j].split('_data')[0].replace('_', ' ').capitalize()
                        greater50 = 1 if w_count > 50 else 0
                        
                        try:
                            opin_author = data['casebody']['data']['opinions'][opin]['author']
                        except:
                            opin_author = ''
                            pass
                        
                        # Concurring or dissenting opinion
                        opin_type = data['casebody']['data']['opinions'][opin]['type']
                        #print(repr(opin_type))
                        
                        # Extract citations in generator object, store in list
                        cite_gen = lexnlp.extract.en.citations.get_citations(data['casebody']['data']['opinions'][opin]['text'], return_source=True, as_dict=True)
                        cite_list = list(cite_gen)
                        
                        # Count # of citations
                        gen_count = len(cite_list)
#                        cite_names = ''
#                        
#                        # Create regex's based on extracted citations
#                        for el in range(0, len(cite_list)):
#                            if el == 0:
#                                cite_names = cite_list[el]['citation_str']
#                            else:
#                                cite_names = cite_names + ', ' + cite_list[el]['citation_str']
                                
#                        # Create list of citation names, Make a regex that matches if any of our regexes match.
#                        cite_list_source = [d['citation_str'] for d in cite_list]
#                        cite_list_source = [e.replace('(', '').replace(')', '') for e in cite_list_source]
#                        cite_list_source = list(set(cite_list_source))
#                        cite_list_source = [a for a in cite_list_source if len(a.split()) < 7]
#                        try:
#                            cite_list_regex = [re.compile(elem) for elem in cite_list_source]
#                        except:
#                            pass
                        
#                        # Sentence parser
#                        sentences = lexnlp.nlp.en.segments.sentences.get_sentence_list(data['casebody']['data']['opinions'][0]['text'].strip())
#                         
#                        pos_cite = 0
#                        neg_cite = 0
#                        
#                        for index, line in enumerate(sentences):
#                            if any(regex.match(line) for regex in cite_list_regex):
#                                #print(sentences[index-1])
#                                sentiment = analyzer.polarity_scores(sentences[index-1])
#                                #print(sentiment)
#                                if sentiment['compound'] > 0.05:
#                                    pos_cite += 1
#                                if sentiment['compound'] > -0.05:
#                                    neg_cite += 1
                     
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
                                           #pos_cites = pos_cite, neg_cites = neg_cite,
                                           flesch = flesch,
                                           flesch_kincaid = flesch_kincaid,
                                           gunning_fog = fog,
                                           smog = smog,
                                           ari = ari,
                                           coleman_liau = coleman_liau,
                                           state = state,
                                           word_count = w_count,
                                           #has_opinion = 1,
                                           total_opins = total_opins,
                                           greater50 = greater50,
                                           opin_author = opin_author,
                                           opin_type = opin_type,
                                           judges = judges)
                        rows_list.append(court_d)
                        
                case_id += 1
            
            
            state_court_d[states[j]] = pd.DataFrame(rows_list)
            #state_court_d[states[j]] = state_court_d[states[j]][columns] # Rearrange columns
            
        t2 = datetime.now()
        print(state + ': ' + str(t2-t1))
    
with open('df_nonmajor_opins.pkl', 'wb') as handle:
    pickle.dump(state_court_d, handle, protocol=pickle.HIGHEST_PROTOCOL)

states_single_df = pd.concat(state_court_d.values(), ignore_index=True)
states_single_df.to_csv('nonmajority_opins.csv', index = False)