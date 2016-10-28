#!/bin/zsh

zcat latitude_longitude_username_createdAt_tweetId.tsv.gz | head -n 20000 | gzip > lat_lon_small.gz
zcat tweets_userid.gz | head -n 20000 | gzip > lat_lon_userid.gz
zcat lat_lon_small.gz | cut -f4 |  while read line; do echo $(TZ=UTC date -d $line "+%s"); done | gzip > lat_lon_unix_timestamp.gz
paste <(zcat lat_lon_small.gz) <(zcat lat_lon_userid.gz ) <(zcat lat_lon_unix_timestamp.gz) | gzip > lat_lon_mixed.gz
# extract userid != 0
zcat lat_lon_mixed.gz | awk -F "\t" '{if ($7 !=0) print}' | gzip > lat_lon_no_0.gz
# sort by user id, then tweet dates
zcat lat_lon_no_0.gz | sort -t$'\t' -k7,7 -k8,8 -n | gzip > lat_lon_sorted.gz
#compute the speed
./compute_speed.py | gzip > lat_lon_speed.gz
