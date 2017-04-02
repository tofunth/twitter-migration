# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:28 2016

@author: tofunth
"""

import gzip
import os

quarter_dict = {'Jan':'01', 'Feb':'01', 'Mar':'01', 'Apr':'02', 'May':'02', 'Jun':'02',
              'Jul':'03', 'Aug':'03', 'Sep':'03', 'Oct':'04', 'Nov':'04', 'Dec':'04'}
              
month_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

prefix = ''
filename = 'ALL_TWEETS_username_date_country_filtered.gz'
filepath = os.path.join(prefix, filename)
fname, fext = os.path.splitext(filepath)
time_level = 2 # 1: quarter level,  2: month level
assert os.path.isfile(filepath) and fext == '.gz'
with gzip.open(filepath, 'rb') as f:
    for line in f:
        line = line.decode('utf-8').strip()
        elem = line.split('\t')
        try:
            tweet_time_elem = elem[1].split()
            tweet_month = tweet_time_elem[1]
            tweet_year = tweet_time_elem[-1]
            if time_level == 1:
                timeval = tweet_year+quarter_dict[tweet_month]
            else:
                timeval = tweet_year+month_dict[tweet_month]
            print timeval
        except Exception:
            print '0'