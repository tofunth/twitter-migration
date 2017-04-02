# %% import packages
import gzip
import json
from sktensor import sptensor
import pickle
import numpy as np
import os
from collections import Counter
window = 3
# %% construct the tensor
# majority filter
def majority_filter_counter(seq, width):
    offset = width // 2
    seq = ['-1'] * offset + seq
    return [Counter(a).most_common(1)[0][0]
        for a in (seq[i:i+width] for i in range(len(seq) - offset))]
# get the flows
def get_travel_flow(filename, country_dic, time_dic):
    last_username = ''
    data = np.zeros((len(country_dic), len(country_dic), len(time_dic)),
                        dtype=int)
    country_timeline = ['-1'] * len(time_dic)
    with gzip.open(filename, 'rb') as f:
        for line in f:
            line = line.decode('utf-8').strip()
            elem = line.split("\t")
            # get userid of the tweet
            username = elem[0]
            # get time of the tweet
            timeval = elem[2]
            # get country of the tweet
            country = elem[1]
            if username!=last_username and last_username != '':
                # interpolate
                start = 0
                end = len(time_dic)
                while country_timeline [start]== '-1': start += 1
                while country_timeline [end-1]== '-1': end -= 1
                for idx in range(start+1, end):
                    if country_timeline[idx] == '-1':
                        country_timeline[idx] = country_timeline[idx-1]
                # majority filter
                # country_timeline[start:end] = majority_filter_counter(country_timeline[start:end], window)
                # update the tensor
                source_count = 0
                dest_count = 1
                source_country = ''
                dest_country = ''
                for idx in range(start+1, end):
                    dest_country = country_timeline[idx] 
                    if dest_country == country_timeline[idx-1]:
                        dest_count += 1
                    else:
                        if source_count >= window and dest_count >= window:
                            data[
                                country_dic[source_country], # source country
                                country_dic[dest_country], # destination country
                                idx # the time of moving
                                ] += 1
                        source_count = dest_count
                        dest_count = 1
                        source_country = dest_country
                # reset country timeline
                country_timeline = ['-1'] * len(time_dic)
            # save the userid and country for the next itereation
            country_timeline[time_dic[timeval]] = country
            last_username = username
    return data
# %% filter data
def filter_data(data, filter_val):
    N, M, K = data.shape
    for i in range(N):
        for j in range(M):
            for k in range(K):
                if data[i][j][k]<filter_val:
                    data[i][j][k] = 0
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
inputname = 'ALL_TWEETS_username_residence_time.gz'
# inputname = 'small.gz'
inputpath = os.path.join(prefix, inputname)
_, fext = os.path.splitext(inputpath)
assert os.path.isfile(inputpath) and fext == '.gz'

filter_val = 0
outputname = 'tensor-rm-3m.dat'
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
data = filter_data(data, filter_val)
save_tensor(data, outputpath)
