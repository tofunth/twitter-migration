# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 12:38:38 2016

@author: tofunth
"""

import gzip
import os

prefix = ''
filename = 'ALL_TWEETS_lat_long_username_date_country_quarter.gz'
filepath = os.path.join(prefix, filename)
fname, fext = os.path.splitext(filepath)
assert os.path.isfile(filepath) and fext == '.gz'
with gzip.open(filepath, 'rb') as f:
    last_username = ''
    last_quarter = ''
    country_counter = {}
    for line in f:
        line = line.decode('utf-8').strip()
        elem = line.split('\t')
        try:
            username = elem[2]
            country = elem[4]
            quarter = elem[5]
            if username == last_username:
                if quarter == last_quarter:
                    if country_counter.has_key(country):
                        country_counter[country] += 1
                    else:
                        country_counter[country] = 1
                else:
                    residence_country, _ = max(country_counter.iteritems(), key=lambda x:x[1])
                    print username+'\t'+last_quarter+'\t'+residence_country
                    country_counter ={country:1}
            else:
                country_counter = {country:1}
                        
            last_username = username
            last_quarter = quarter
        except Exception as e:
            print '0'
        