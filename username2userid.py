#!/usr/bin/env python
import gzip

# build dictionary
username_dict = {}
with gzip.open("userid_username.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        elements = line.split()
        username_dict[elements[1]] = elements[0]
        
# output the file
with gzip.open("tweets_username.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        print(username_dict.get(line, "0"))