#!/usr/bin/env python
import gzip
from sktensor import sptensor
import pickle

filename = "date_country_userid.gz"
month_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

country_lst = []
yearmonth_lst = []

with gzip.open(filename, 'rb') as f:
    for line in f:
        line = line.decode('utf-8').strip()
        elems = line.split("\t")
        date = elems[0].split(" ")
        yearmonth = date[-1]+month_dict[date[1]]
        if yearmonth not in yearmonth_lst:
            yearmonth_lst.append(yearmonth)

        country = elems[1]
        if country not in country_lst:
            country_lst.append(country)

yearmonth_lst.sort()
country_lst.sort()

yearmonth_dic = {yearmonth_lst[i]:i
                      for i in range(len(yearmonth_lst))}
                          
country_dic = {country_lst[i]:i
                    for i in range(len(country_lst))}

# get the flows
prev_userid = ''
prev_country = ''
col_dic = {}

with gzip.open(filename, 'rb') as f:
    for line in f:
        line = line.decode('utf-8').strip()
        elems = line.split("\t")
        # get yearmonth of the tweet
        date = elems[0].split(" ")
        yearmonth = date[-1]+month_dict[date[1]]
        # get country of the tweet
        country = elems[1]
        # get userid of the tweet
        userid = elems[2]
        if userid==prev_userid and country!=prev_country:
            col_val = (prev_country, country, yearmonth)
            if col_val in col_dic.keys():
                col_dic[col_val] += 1
            else:
                col_dic[col_val] = 1
        # save the userid and country for the next itereation
        prev_userid = userid
        prev_country = country
        
# build the sparse tensor
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
with open('tensor.dat', 'wb') as f:
    pickle.dump(T, f)