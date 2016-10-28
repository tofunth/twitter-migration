#!/bin/zsh
# cut the neccesary fields
zcat userinfo_users_with_more_than_one_country.txt.gz | cut -f 1,6,7,8,9 | gzip > users_stats.gz
# extract the creation date field, convert to unix timestamp, write
zcat users_stats.gz | cut -f 5 | while read line; do echo $(TZ=UTC date -d $line "+%s"); done | gzip > users_stats_unix_timestamp.gz
# concatenate with the stats file
paste <(zcat users_stats.gz) <(zcat users_stats_unix_timestamp.gz) | gzip > users_stats_mixed.gz
# extract user ids with followers less than sth
zcat users_stats_mixed.gz | awk '{if ($2 <10) print $1}' | gzip > users_followers_less.gz
# extract user ids with friends less than sth
zcat users_stats_mixed.gz | awk '{if ($3 <10) print $1}' | gzip > users_friends_less.gz
# find max and min date
zcat users_stats_mixed.gz| awk -F "\t" 'BEGIN{min=1e16;max=-1e16} {if ($6<min) min=$6; if ($6>max) max=$6} END{print "min=", min, "max=", max}'
# extract user ids with creation date less than 1 year after 01.10.2015
zcat users_stats_mixed.gz | awk -F "\t" '{if ($6 > 1475280000) print $1}' | gzip > users_creationdate_less.gz
# get the removing candidates
./remove_candiates.py | gzip > users_remove_candidates.gz
