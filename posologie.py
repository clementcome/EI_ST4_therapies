import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def length_activity(activity):
    with open('data/des.json') as json_es:
        es = json.load(json_es)
    duree = 0
    if

def mean_time_between_two_connexions(ID):
    '''
    :param ID: key to identify a user
    :return: number of connexions of the user
    '''
    with open('data/des.json') as json_es:
        es = json.load(json_es)
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                debut = es[event]["type"]["date"]
                end = debut + es[event]["type"]["data"]["duration"]
                date_activities_completed.append((debut,end))
    date_activities_completed.sort()
    number_connexions = 1
    for i in range(len(date_activities_completed)-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            number_connexions += 1
    return (number_connexions)



def posologie(data):

