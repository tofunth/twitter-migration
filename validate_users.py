#!/usr/bin/env python

import gzip

# build dictionary
username_dict = {}
with gzip.open("userid_username.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        elements = line.split()
        username_dict[elements[0]] = elements[1]
        
remove_users = []
keep_users = []

with gzip.open("validate_remove_users.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        remove_user = username_dict.get(line)
        remove_users.append(remove_user)
        
with gzip.open("validate_keep_users.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        keep_user = username_dict.get(line)
        keep_users.append(keep_user)
        
import botornot
twitter_app_auth = {
    'consumer_key': 'xxxx',
    'consumer_secret': 'xxxx',
    'access_token': 'xxxx',
    'access_token_secret': 'xxxx',
}

bon = botornot.BotOrNot(**twitter_app_auth)
remove_users_results = []
keep_users_results = []

for u in remove_users:
    try:
        res = bon.check_account(u)
        remove_users_results.append(res)
    except Exception:
        pass
    
for u in keep_users:
    try:
        res = bon.check_account(u)
        keep_users_results.append(res)
    except Exception:
        pass
    
# plot the results
import matplotlib.pyplot as plt

remove_users_scores = [u['score'] for u in remove_users_results]
keep_users_scores = [u['score'] for u in keep_users_results]

plt.figure(1)
plt.subplot(211)
plt.hist(x = remove_users_scores, bins=50)
plt.xlabel('score')
plt.ylabel('count')
plt.title('Bot likelihood score of removing users')
plt.subplot(212)
plt.hist(x = keep_users_scores, bins=50)
plt.xlabel('score')
plt.ylabel('count')
plt.title('Bot likelihood score of keeping users')
