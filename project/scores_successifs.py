import json
import matplotlib.pyplot as plt
import pandas
import numpy as np


#scores successifs pour une activité [ des[data][gameScore] + des[userKey] where des[type] = “ACTIVITY_COMPLETE” ]
def score(file="data/data_activity.json"):
    users={}
    with open(file) as input_file:
        data = json.load(input_file)["es"]
    #print(data)
    for des in data.keys():
        print(des)
        if data[des]["type"]=='ACTIVITY_COMPLETE':
            if data[des]["userKey"] not in users.keys():
                # print(data[des])
                # print(data[des]["userKey"])
                # print(users)
                try:
                    users[data[des]["userKey"]]=[]  #Liste qui contiendra les score et leur date
                    users[data[des]["userKey"]].append([data[des]["data"]["gameScore"],(data[des]["date"])])
                except:
                    pass
            else:
                users[data[des]["userKey"]].append([data[des]["data"]["gameScore"],(data[des]["date"])])
    return users

print (score())
