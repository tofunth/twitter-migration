#!/bin/zsh

# sample removal users
zcat users_remove_candidates.gz | shuf -n 90 | gzip > validate_remove_users.gz

# sample keep users
zcat tweets_lat_lon_final.gz | cut -f 7 | shuf -n 90 | gzip > validate_keep_users.gz
