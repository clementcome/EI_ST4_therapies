import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

def create_dictionnaries(file_path):
    with open(file_path) as json_data:
        data = json.load(json_data)
        es = data["es"]
        su = data["su"]
    return (es,su)

def number_of_connexions_per_day(ID, file_path, es = None):
    '''
    :param ID: user_key
    :param file_path
    :return: list with the number of connexions each day since the first use of Diapason
    '''
    if es == None:
        es = create_dictionnaries(file_path)[0]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                try :
                    debut = es[event]["date"]
                    end = debut + es[event]["data"]["duration"]
                    date_activities_completed.append((debut,end))
                except :
                    pass
    date_activities_completed.sort()
    if date_activities_completed == []:
        return []
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities - 1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    first_connexion = date_connexion[0]
    number_connexions = len(date_connexion)
    for i in range(number_connexions):
        date_connexion[i] -= first_connexion
    number_of_days = date_connexion[-1]//(3600*24)
    connexion_days = [0]*number_of_days
    index_day = 0
    index_connexion = 0
    upper_bound = 3600*24
    while index_day < number_of_days and index_connexion < len(date_connexion):
        if date_connexion[index_connexion] < upper_bound :
            connexion_days[index_day] += 1
            index_connexion += 1
        else :
            upper_bound += 3600*24
            index_day += 1
    return connexion_days


def plot_connexion(ID, file_path, es=None):
    '''
    :param ID:
    :param file_path:
    :return: a plot of the number of connexions per day of ID
    '''
    connexion_days = number_of_connexions_per_day(ID,file_path,es)
    X = np.arange(len(connexion_days))
    plt.plot(X,connexion_days, color = 'turquoise')
    plt.ylabel("Number of connexions")
    plt.xlabel("Number of days")
    # plt.title("Number of connexions per day since first connexion of {}".format(ID))
    plt.show()

def maximum_length_dictionnary(dict):
    max = 0
    for value in dict.values():
        if len(value) > max:
            max = len(value)
    return max

def number_of_connexions_per_day_global(file_path,es=None,su=None):
    '''
    :param file_path:
    :return: list with the normalized number of connexions per day of each user from the first day of connexion
    '''
    if es == None or su == None:
        (es, su) = create_dictionnaries(file_path)
    connexions_per_day = {}
    for ID in su.keys():
        nb = number_of_connexions_per_day(ID,file_path,es)
        if not nb == [] :
            connexions_per_day[ID] = nb
    max_seniority = maximum_length_dictionnary(connexions_per_day)
    nb_connexions_per_day = [0] * max_seniority
    nb_users_per_day = [0] * max_seniority
    for user in connexions_per_day.values():
        for i in range(len(user)):
            nb_connexions_per_day[i] += user[i]
            nb_users_per_day[i] += 1
    for i in range(max_seniority) :
        nb_connexions_per_day[i] = nb_connexions_per_day[i]/nb_users_per_day[i]
    return nb_connexions_per_day


def plot_connexion_global(file_path):
    '''
    :param file_path:
    :return: a plot of the normalized number of connexions per day since first day of connexion
    '''
    connexion_days = number_of_connexions_per_day_global(file_path)
    X = np.arange(len(connexion_days))
    plt.plot(X,connexion_days, color = 'turquoise')
    plt.ylabel("Number of connexions")
    plt.xlabel("Number of days since day 1")
    plt.show()


def time_between_connexions(ID,file_path,es=None):
    '''
    :param ID: user_key
    :param file_path
    :return: a list of the time in hour elapsed between successive connexions of ID
    '''
    if es == None:
        es = create_dictionnaries(file_path)[0]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                try :
                    debut = es[event]["date"]
                    end = debut + es[event]["data"]["duration"]
                    date_activities_completed.append((debut,end))
                except :
                    pass
    if date_activities_completed == []:
        return []
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities - 1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    time_between_connexions = []
    for i in range(len(date_connexion)-1):
        delta = date_connexion[i+1] - date_connexion[i]
        time_between_connexions.append(delta//(3600*24))
    return time_between_connexions

def plot_time_between_connexion(ID, file_path,es=None):
    '''
    :param ID
    :param file_path
    :return: a plot of the time between two connexions
    '''
    time_between_connexion = time_between_connexions(ID,file_path,es)
    X = np.arange(len(time_between_connexion))
    plt.bar(X,time_between_connexion)
    plt.ylabel("Time between connexions (days)")
    plt.xlabel("Connexions")
    plt.xticks(X)
    plt.show()


def time_between_connexions_global(file_path, es=None, su=None):
    '''
    :param file_path
    :return: a list of the time in hour elapsed between successive connexions of ID
    '''
    median_times = []
    if es == None or su == None:
        (es, su) = create_dictionnaries(file_path)
    for ID in su.keys():
        time = time_between_connexions(ID,file_path,es)
        if not time == []:
            median = np.median(time)
            median_times.append(median)
    return median_times


def plot_time_between_connexion_global(file_path):
    '''
    :param file_path
    :return: a plot of the median times between connexions
    '''
    time_between_connexion = time_between_connexions_global(file_path)
    bins = [2**i for i in range(8)]
    plt.hist(time_between_connexion,bins=bins)
    plt.xlabel("Median time between connexions (days)")
    plt.ylabel("Users")
    plt.xscale("log")
    plt.show()


def number_activities_per_connexion(ID, file_path,es=None):
    '''
    :param ID: user_key
    :param file_path
    :return: a list with the number of activities per connexion
    '''
    if es == None:
        es = create_dictionnaries(file_path)[0]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                try :
                    debut = es[event]["date"]
                    end = debut + es[event]["data"]["duration"]
                    date_activities_completed.append((debut,end))
                except :
                    pass
    date_activities_completed.sort()
    number_activities_per_connexion = []
    number_activities = len(date_activities_completed)
    count_activity = 1
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            number_activities_per_connexion.append(count_activity)
            count_activity = 1
        else :
            count_activity += 1
    number_activities_per_connexion.append(number_activities - sum(number_activities_per_connexion))
    return number_activities_per_connexion


def plot_number_activities_per_connexion(ID, file_path, es=None):
    '''
    :param ID: user key
    :param file_path
    :return: plot the number of activities per connexion
    '''
    number_activities = number_activities_per_connexion(ID, file_path, es)
    X = np.arange(len(number_activities))
    plt.bar(X,number_activities)
    plt.ylabel("Number of activities per connexion")
    plt.xlabel("Connexions")
    plt.xticks(X)
    plt.show()

def number_activities_per_connexion_global(file_path, es=None, su=None):
    '''
    :param file_path
    :return: a list with the mean number of activities per connexion for each user
    '''
    if es == None or su == None:
        (es, su) = create_dictionnaries(file_path)
    mean_numbers = []
    for ID in su :
        nb = number_activities_per_connexion(ID, file_path, es)
        if not nb == []:
            mean = np.mean(nb)
            mean_numbers.append(mean)
    return(mean_numbers)

def plot_number_activities_per_connexion_global(file_path, es = None, su=None):
    '''
    :param file_path:
    :return: a plot of the number of activities per connexion for each user
    '''
    nb = number_activities_per_connexion_global(file_path,es,su)
    plt.hist(nb)
    plt.ylabel("Users")
    plt.xlabel("Mean number of activities per connexion")
    plt.show()









