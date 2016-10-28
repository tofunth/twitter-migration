#!/usr/bin/env python
import gzip
from math import cos, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def sec2hour(new_sec, old_sec):
    mul = 0.0002777777777777778
    return mul*float(new_sec-old_sec)

old_lat = 0.
old_lon = 0.
old_user = 0
old_sec = 0
with gzip.open("lat_lon_sorted.gz", "rb") as f:
    for line in f:
        line = line.decode("utf-8").strip()
        elements = line.split("\t")
        this_lat = float(elements[0])
        this_lon = float(elements[1])
        this_user = int(elements[6])
        this_sec = int(elements[7])
        if this_user == old_user:
            dist = distance(this_lat, this_lon, old_lat, old_lon)
            tim = sec2hour(this_sec, old_sec)
            if tim!=0: 
                print(int(dist/tim)) 
            else:
                if dist<50.0:
                    print("0")
                else:
                    print('9999999')
        else:
            print(0)
        old_lat = this_lat
        old_lon = this_lon
        old_user = this_user
        old_sec = this_sec
        