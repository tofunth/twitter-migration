#!/usr/zsh

# create the splitting directory
mkdir data/split
# split the data into 5M-line chunks
zcat data/ALL_TWEETS_lat_long_username_date_country.gz | split -l 5000000 --filter='gzip > $FILE.gz' - data/split/
