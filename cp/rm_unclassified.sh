#!/bin/zsh

# remove tweets with fail-computed locations
zcat ALL_TWEETS_lat_long_username_date_country.gz | awk -F "\t" '{if ($5 != "-99") print}' | gzip > clean.gz
# overwrite the field-extracted tweets
mv clean.gz ALL_TWEETS_lat_long_username_date_country.gz
