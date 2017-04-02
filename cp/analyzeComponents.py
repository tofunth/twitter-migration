import numpy as np
import matplotlib.pyplot as plt
import json
import os
from gini.gini import gini
import pycountry
k = 50
top_k = 50
top_country = 10
result = np.load('bptf/code/rm-3m-k50/1_trained_model.npz')

# get the matrices
E_DK_M = result['E_DK_M']

source = E_DK_M[0]
dest = E_DK_M[1]
time = E_DK_M[2]
# %% load dictionary
def load_dic(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

# %% get top n values in an array
def get_top(array, n):
    array = array.flatten()
    return sorted(range(len(array)), key=lambda i:array[i])[-n:]
# %% dictionaries 
prefix = 'data'
figprefix = 'rm-3m-k50'
dicname = 'dic.json'
dicpath = os.path.join(prefix, dicname)
_, fext = os.path.splitext(dicpath)
assert fext == '.json'

dic = load_dic(dicpath)
country_dic = dic['country_dic']
time_dic = dic['time_dic']
# %% main
n_time = time.shape[0]
n_country = dest.shape[0]

time_gini = np.array([gini(time[:,i]) for i in range(k)])
time_top = get_top(time_gini, top_k)
time_lab = sorted(time_dic.keys())

time_lab = [label[:4]+'/'+label[4:] for label in time_lab]

# plot time
idx = 0
for j in time_top[::-1]:
    fig = plt.figure(figsize=(18,8))
    ax0 = fig.add_subplot(2, 1, 1)
    ax0.set_xticks(range(n_time))
    ax0.set_xticklabels(time_lab, rotation=70, fontsize=22)
    for label in ax0.xaxis.get_ticklabels()[::]:
        label.set_visible(False)
    for label in ax0.xaxis.get_ticklabels()[::4]:
        label.set_visible(True)
    ax0.set_title('Time-step factor', fontsize=18)
    ax0.plot(range(17,n_time), time[17:, j])
    
    # plot country
    source_comp = source[:, j]
    dest_comp = dest[:, j]
    
    source_idx = get_top(source_comp, top_country)
    dest_idx = get_top(dest_comp, top_country)
    
    source_val = [source_comp[i] for i in source_idx]
    dest_val = [dest_comp[i] for i in dest_idx]
    
    countries = sorted(country_dic.keys())
    
    source_lab = [pycountry.countries.get(alpha_2=countries[i].upper()).name for i in source_idx]
    dest_lab = [pycountry.countries.get(alpha_2=countries[i].upper()).name for i in dest_idx]
    ax1 = fig.add_subplot(2, 2, 3)
    ax1.grid()
    ax1.set_xticks(range(top_country))
    ax1.set_xticklabels(source_lab, rotation=65, fontsize=18)
    ax1.set_title('Top-10 origin country factor', fontsize=20)
    ax1.bar(range(top_country), source_val)
    
    ax2 = fig.add_subplot(2, 2, 4)
    ax2.grid()
    ax2.set_xticks(range(top_country))
    ax2.set_xticklabels(dest_lab, rotation=65, fontsize=18)
    ax2.set_title('Top-10 destination country factor', fontsize=20)
    ax2.bar(range(top_country), dest_val)
    
    plt.tight_layout()
    figname = 'component '+'%02d'%idx+'.pdf'
    figpath = os.path.join(prefix, figprefix, figname)
    fig.savefig(figpath)
    plt.close(fig)
    
    idx += 1
