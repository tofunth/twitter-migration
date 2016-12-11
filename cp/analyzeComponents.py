import numpy as np
import matplotlib.pyplot as plt
import json
import os
from gini.gini import gini
k = 50
top_k = 50
top = 10
result = np.load('bptf/code/k50/1_trained_model.npz')

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

# plot time
idx = 0
for j in time_top[::-1]:
    fig = plt.figure(figsize=(7, 9))
    fig.subplots_adjust(hspace=1)
    ax0 = fig.add_subplot(3, 1, 1)
    ax0.set_xticks(range(n_time))
    ax0.set_xticklabels(time_lab, rotation=45)
    ax0.plot(range(n_time), time[:, j])
    
    # plot country
    source_comp = source[:, j]
    dest_comp = dest[:, j]
    
    source_idx = get_top(source_comp, top)
    dest_idx = get_top(dest_comp, top)
    
    source_val = [source_comp[i] for i in source_idx]
    dest_val = [dest_comp[i] for i in dest_idx]
    
    countries = sorted(country_dic.keys())
    
    source_lab = [countries[i] for i in source_idx]
    dest_lab = [countries[i] for i in dest_idx]
    ax1 = fig.add_subplot(3, 1, 2)
    ax1.set_xticks(range(top))
    ax1.set_xticklabels(source_lab)
    ax1.bar(range(top), source_val)
    
    ax2 = fig.add_subplot(3, 1, 3)
    ax2.set_xticks(range(top))
    ax2.set_xticklabels(dest_lab)
    ax2.bar(range(top), dest_val)
    
    figname = 'component '+'%02d'%idx+'.eps'
    figpath = os.path.join(prefix, figname)
    fig.savefig(figpath)
    plt.close(fig)
    
    idx += 1
