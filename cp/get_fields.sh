#!/bin/zsh

# get date, country, and usid fields from the tweets
zcat tweets_lat_lon_final.gz | cut -f4,6,7 | gzip > date_country_userid.gz
# remove tweets with fail-computed locations
zcat date_country_userid.gz | awk -F "\t" '{if ($2 != "-99") print}' | gzip > date_country_userid_clean.gz
# overwrite the field-extracted tweets
mv date_country_userid_clean.gz date_country_userid.gz
