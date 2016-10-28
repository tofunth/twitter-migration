import matplotlib.pyplot as plt
from datetime import datetime
import gzip

followers = []
friends = []
statuses = []
creationtime = []
creationtime2 = []

with gzip.open('users_stats_mixed.gz', 'rb') as f:
    for line in f:
        line = line.decode('utf-8').strip()
        elements = line.split('\t',5)
        followers.append(int(elements[1]))
        friends.append(int(elements[2]))
        statuses.append(int(elements[3]))
        creationtime.append(
            int(datetime.timestamp(
                datetime.strptime(elements[4], "%a %b %d %H:%M:%S %z %Y")
            ))
        )
        creationtime2.append(int(elements[5]))
        
plt.figure(1)
plt.subplot(221)
plt.hist(x=followers, bins=100, range=(0, 4000))
plt.xlabel("Followers number")
plt.ylabel("Count")
plt.subplot(222)
plt.hist(x=friends, bins=100, range=(0, 2000))
plt.xlabel("Friends number")
plt.ylabel("Count")
plt.subplot(223)
plt.hist(x=statuses, bins=100, range=(0, 100))
plt.xlabel("Status number")
plt.ylabel("Count")
plt.subplot(224)
plt.hist(x=creationtime, bins=100)
plt.xlabel("Creation date")
plt.ylabel("Count")
plt.show()