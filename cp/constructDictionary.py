# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:30:21 2016

@author: tofunth
"""
# %% import some packages
import gzip
import os
import json
# %% compute the dictionaries from file    
def get_dic(filename):             
    country_lst = []
    time_lst = []
    with gzip.open(filename, 'rb') as f:
        for line in f:
            try:
                line = line.decode('utf-8').strip()
                elem = line.split("\t")
                
                quarter = elem[1]
                country = elem[2]
                if quarter not in time_lst:
                    time_lst.append(quarter)
    
                if country not in country_lst:
                    country_lst.append(country)
            except Exception as e:
                print e.message
    
    time_lst.sort()
    country_lst.sort()
    
    time_dic = {time_lst[i]:i
                          for i in range(len(time_lst))}
                              
    country_dic = {country_lst[i]:i
                        for i in range(len(country_lst))}    
    return (country_dic, time_dic)

# %% save file
def save_file(filename, country_dic, time_dic):
    with open(filename, 'w') as f:
        result = {'country_dic': country_dic, 'time_dic': time_dic}
        json.dump(result, f)
# %% main script
prefix = 'data'
inputname = 'ALL_TWEETS_username_quarter_residence.gz'
inputpath = os.path.join(prefix, inputname)
_, fext = os.path.splitext(inputpath)
assert os.path.isfile(inputpath) and fext == '.gz'

outputname = 'dic.json'
outputpath = os.path.join(prefix, outputname)
_, fext = os.path.splitext(outputpath)
assert fext == '.json'

# get the dictionaries from input
country_dic, time_dic = get_dic(inputpath)
# save the result
save_file(outputpath, country_dic, time_dic)