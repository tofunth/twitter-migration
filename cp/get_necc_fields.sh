#!/bin/zsh

# get date, country, and usid fields from the tweets
zcat ALL_TWEETS_latitude_longitude_username_createdAt_tweetId.tsv.gz | cut -f1,2,3,4,6 | gzip > ALL_TWEETS_lat_long_username_date_country.gz
