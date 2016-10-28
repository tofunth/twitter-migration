#!/bin/zsh
# make a dict of userid and username
zcat userinfo_users_with_more_than_one_country.txt.gz | cut -f 2,1 | awk '{print tolower($0)}' | gzip > userid_username.gz
# extract the username from tweets
zcat latitude_longitude_username_createdAt_tweetId.tsv.gz | cut -f 3 | awk '{print tolower($0)}'| gzip > tweets_username.gz
# repace username with userid, using an additional python script
./username2userid.py | gzip > tweets_userid.gz
# output some stats
zcat tweets_userid.gz| sort | uniq -c | sort -nr | gzip > tweets_userid_stats.gz
