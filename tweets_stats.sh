#!/bin/zsh

# paste the userid matching to userinfo, 0 mean not found
paste <(zcat latitude_longitude_username_createdAt_tweetId.tsv.gz) <(zcat tweets_userid.gz) | gzip > tweets_lat_lon_userid.gz
# remove the tweets having the owner not in the userinfo
zcat tweets_lat_lon_userid.gz | awk -F "\t" '{if ($7 !=0) print}' | gzip > tweets_lat_lon_no0.gz
# extract the creation date, convert to unix time stamp and save
zcat tweets_lat_lon_no0.gz | cut -f4 |  while read line; do echo $(TZ=UTC date -d $line "+%s"); done | gzip > tweets_lat_lon_unix_timestamp.gz
# paste unix timestamp to no0 -> mixed
paste <(zcat tweets_lat_lon_no0.gz) <(zcat tweets_lat_lon_unix_timestamp.gz) | gzip > tweets_lat_lon_mixed.gz
# sort by userid, then tweet dates
zcat tweets_lat_lon_mixed.gz | sort -t$'\t' -k7,7 -k8,8 -n | gzip > tweets_lat_lon_sorted.gz
#compute all the speeds b/w two consecutive tweets belonging to each unique users
./compute_speed.py | gzip > tweets_lat_lon_speed.gz
# stack the speed the data
paste <(zcat tweets_lat_lon_sorted.gz) <(zcat tweets_lat_lon_speed.gz) | gzip > tweets_lat_lon_speed_mixed.gz
# remove all tweets with changing location speed more than 1000
zcat tweets_lat_lon_speed_mixed.gz | awk -F "\t" '{if ($9 < 1000) print}' | gzip > tweets_lat_lon_no_more_1000.gz
# change the name to "mixed"
# remove tweets from removal candidates

