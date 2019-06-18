import json
import matplotlib.pyplot as plt


def tinnituses_features(data):
    with open(data) as json_es:
        abon = json.load(json_es)
    tinnituse = []
    count_error = 0
    for user in abon :
        try :
            frequence = abon[user]["reducers"]["tinnituses"][0]["frequency"]
            bandwidth = abon[user]["reducers"]["tinnituses"][0]["bandwidth"]
            tinnituse.append((frequence, bandwidth))
        except :
            count_error += 1
    return(tinnituse,count_error)


tinnituse = tinnituses_features('data/dsu.json')[0]

X = [val[0] for val in tinnituse]
Y = [val[1] for val in tinnituse]
plt.xlabel("Frequences")
plt.ylabel("Bandwith")
plt.scatter(X,Y, color='fuchsia')
plt.show()










