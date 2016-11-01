#!/usr/bin/env python
import gzip

# build lookup table
removing_users = set()
with gzip.open("users_remove_candidates.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        removing_users.add(line)
        
with gzip.open("tweets_lat_lon_mixed.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        elements = line.split("\t")
        userid = elements[6]
        if userid not in removing_users:
            print(line)