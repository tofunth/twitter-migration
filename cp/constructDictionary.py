# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:30:21 2016

@author: tofunth
"""
# %% import some packages
from path import path
from argparse import ArgumentParser
import gzip
import json
import inspect
# %% local variables for debugging
local_vars = {}
# %% compute the dictionaries from file
def get_dic(filename):   
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
    return (country_dic, yearmonth_dic)

# %% save file
def save_file(filename, country_dic, yearmonth_dic):
    with open(filename, 'w') as f:
        result = {'country_dic': country_dic, 'yearmonth_dic': yearmonth_dic}
        json.dump(result, f)
# %% main script
def main():
    global local_vars
    
    p = ArgumentParser()
    p.add_argument('-i', '--input', type=path, required=True)
    p.add_argument('-o', '--output', type=path, required=True)
    
    args = p.parse_args()
    assert args.input.exists()
    assert args.input.ext == '.gz'
    assert args.output.ext == '.json'
    
    # get the dictionaries from input
    country_dic, yearmonth_dic = get_dic(args.input)
    # save the result
    save_file(args.output, country_dic, yearmonth_dic)
    # for debugging in Spyder
    local_vars = inspect.currentframe().f_locals
    

if __name__ == '__main__':
    main()