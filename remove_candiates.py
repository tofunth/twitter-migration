#!/usr/bin/env python
import gzip

friends_less = set()
followers_less = set()
creationdate_less = set()

with gzip.open("users_friends_less.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        friends_less.add(line)
        
with gzip.open("users_followers_less.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        followers_less.add(line)
        
with gzip.open("users_creationdate_less.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        creationdate_less.add(line)
        
remove_candidates = friends_less | followers_less | creationdate_less

for rc in remove_candidates:
    print(rc)