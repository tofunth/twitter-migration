# %% import packages
import gzip
import json
from sktensor import sptensor
import pickle
import numpy as np
import os
# %% construct the tensor
# get the flows
def get_travel_flow(filename, country_dic, time_dic):
    last_username = ''
    last_country = ''
    data = np.zeros((len(country_dic), len(country_dic), len(time_dic)),
                        dtype=int)
    
    with gzip.open(filename, 'rb') as f:
        for line in f:
            line = line.decode('utf-8').strip()
            elem = line.split("\t")
            # get userid of the tweet
            username = elem[0]
            # get time of the tweet
            quarter = elem[1]
            # get country of the tweet
            country = elem[2]
            if username==last_username and country!=last_country:
                data[
                    country_dic[country], # source country
                    country_dic[last_country], # destination country
                    time_dic[quarter]
                    ] += 1
            # save the userid and country for the next itereation
            last_username = username
            last_country = country
    return data

'''
# %% build the sparse tensor
src_row = []
dest_row = []
time_row = []
vals = []
for col_val, count in col_dic.items():
    src_row.append(country_dic[col_val[0]])
    dest_row.append(country_dic[col_val[1]])
    time_row.append(yearmonth_dic[col_val[2]])
    vals.append(count)
    
subs = (src_row, dest_row, time_row)
tensor_dim = (len(country_dic), len(country_dic), len(yearmonth_dic))
T = sptensor(subs=subs, vals=vals, shape=tensor_dim, dtype=int)

# serialize the tensor
with open('tensor.dat', 'w+') as f:
    pickle.dump(T, f)
'''
# %% serialize the data
def save_tensor(data, filename):
    with open(filename, 'w+') as f:
        pickle.dump(data, f)
# %% load dictionary
def load_dic(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())
# %% main script
prefix = 'data'
inputname = 'ALL_TWEETS_username_quarter_residence.gz'
inputpath = os.path.join(prefix, inputname)
_, fext = os.path.splitext(inputpath)
assert os.path.isfile(inputpath) and fext == '.gz'

outputname = 'tensor.dat'
outputpath = os.path.join(prefix, outputname)
_, fext = os.path.splitext(outputpath)
assert fext == '.dat'

dicname = 'dic.json'
dicpath = os.path.join(prefix, dicname)
_, fext = os.path.splitext(dicpath)
assert fext == '.json'

dic = load_dic(dicpath)
country_dic = dic['country_dic']
time_dic = dic['time_dic']
data = get_travel_flow(inputpath, country_dic, time_dic)
save_tensor(data, outputpath)
