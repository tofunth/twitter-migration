#!/bin/zsh

# extract the creation date, convert to unix time stamp and save
zcat latitude_longitude_username_createdAt_tweetId.tsv.gz | cut -f4 |  while read line; do echo $(TZ=UTC date -d $line "+%s"); done | gzip > tweets_unix_timestamp.gz
# 
