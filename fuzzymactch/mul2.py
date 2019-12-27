
import pandas as pd
import time
from fuzzywuzzy import fuzz
from collections import Counter
from multiprocessing import Process
from multiprocessing import Queue

import csv
import os


# if os.path.exists('./company_in_solr.csv'):
#   os.remove('./company_in_solr.csv')
# else:
#   print("The file does not exist")

pd.set_option('display.max_columns', 1000)
df = pd.read_csv("./source.csv")
df.head()


all_names = df['Name'].unique()

all_main_name = pd.DataFrame(columns=['sort_gp','names','alias','score'])
all_names.sort()
all_main_name['names'] = all_names
all_main_name['sort_gp'] = all_main_name['names'].apply(lambda x: x[0])

all_sort_gp = all_main_name['sort_gp'].unique()

time_start=time.time()


names_freq = Counter()
for name in all_names:
    names_freq.update(str(name).split(" "))
key_words = [word for (word,_) in names_freq.most_common(30)]


def handleOneDate(i,gp_end,all_main_name):
    # if self has not got alias, asign to be alias of itself


    if pd.isna(all_main_name['alias'].iloc[i]):
        all_main_name['alias'].iloc[i] = all_main_name['names'].iloc[i]
        all_main_name['score'].iloc[i] = 100

    # if the following has not got alias and fuzzy match, asign to be alias of this one
    for j in range(i+1,gp_end+1):
        if pd.isna(all_main_name['alias'].iloc[j]):
            fuzz_socre = fuzz.token_sort_ratio(all_main_name['names'].iloc[i],all_main_name['names'].iloc[j])

            if not no_key_word(all_main_name['names'].iloc[j]):
                fuzz_socre -= 10
                
            if (fuzz_socre > 80):
                all_main_name['alias'].iloc[j] = all_main_name['alias'].iloc[i]
                all_main_name['score'].iloc[j] = fuzz_socre



    if i % (len(all_names)//100) == 0:
        process = 100*i/len(all_names)

        if process > 0:
            time_end=time.time()
            cost_sec = time_end-time_start
            cost = int(cost_sec/60)
            remain = int(((cost_sec / (process/100)) - cost_sec) / 60)

            str = "progress: %.2f" % process + "% " + 'Current cost %s' % cost +" mins " + 'Remain cost %s' % remain +" mins " 
            print(str)



def no_key_word(name):
    """check if the name contain the keywords in travel company"""
    output = True
    for key in key_words:
        if key in name:
            output = False
    return output


for sortgp in all_sort_gp:
    this_gp = all_main_name.groupby(['sort_gp']).get_group(sortgp)
    gp_start = this_gp.index.min()
    gp_end = this_gp.index.max()

    # proc_record = []

    for i in range(gp_start,gp_end+1):
        p = Process(target=handleOneDate, args=(i,gp_end,all_main_name))
        p.start() 
        p.join()
        # print(1)

        
all_main_name.to_csv('./company_in_solr.csv')         


