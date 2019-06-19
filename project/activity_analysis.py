import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


def mean_time_between_connexions(ID,file):
    '''
    :param ID: user_key
    :param file: file with data
    :return:
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        es = data["es"]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                debut = es[event]["date"]
                end = debut + es[event]["data"]["duration"]
                date_activities_completed.append((debut,end))
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    time_between_connexions = []
    for i in range(len(date_connexion)-1):
        delta = date_connexion[i+1] - date_connexion[i]
        time_between_connexions.append(delta)
    #mean = np.mean(time_between_connexions)//3600
    #if mean >= 48 :
        #mean = np.mean(time_between_connexions)//(3600*24)
        #return ("Le temps moyen entre deux connexions est {} jours".format(mean))
    #return ("Le temps moyen entre deux connexions est {} heures".format(mean))
    return np.mean(time_between_connexions)


def mean_time_between_connexions_test(ID,file):
    '''
    :param ID: user_key
    :param file: file with data
    :return:
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        es = data["es"]
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
        return 0
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    time_between_connexions = []
    for i in range(len(date_connexion)-1):
        delta = date_connexion[i+1] - date_connexion[i]
        time_between_connexions.append(delta)
    if time_between_connexions == []:
        return 0
    mean = np.mean(time_between_connexions)//3600
    if mean >= 48 :
        mean = np.mean(time_between_connexions)//(3600*24)
        #return ("Le temps moyen entre deux connexions est {} jours".format(mean))
    #return ("Le temps moyen entre deux connexions est {} heures".format(mean))
    return np.mean(time_between_connexions)


def mean_time_connexions(file):
    '''
    :param file: file with data
    :return:
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        su = data["su"]
    means = []
    for ID in su.keys():
        m = mean_time_between_connexions_test(ID,file)
        if m != 0 :
            means.append(m)
    X = np.arange(len(means))
    plt.plot(X,means, color = 'turquoise')
    plt.ylabel("Number of connexions")
    plt.xlabel("User")
    # plt.title("Number of connexions per day since first connexion of {}".format(ID))
    # Mettre de meilleurs noms de graphes
    plt.show()


def mean_time_between_connexions_global(file):
    '''
    :param file: file with data
    :return: plot a histogram
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        su = data["su"]
    means = []
    for ID in su.keys():
        m = mean_time_between_connexions_test(ID,file)
        if m != 0 :
            means.append(m)
    plt.title('Fréquence de connexion inférieure au temps préconisé ', fontsize=10)
    plt.xlabel('Durée moyenne entre deux connexions')
    plt.ylabel("Nombre d'utilisateurs")
    plt.hist(means)
    plt.show()


def connexions_date(ID,file):
    '''
    :param ID: user_key
    :param file: file with data
    :return: list with data time
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        es = data["es"]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                debut = es[event]["date"]
                end = debut + es[event]["data"]["duration"]
                date_activities_completed.append((debut,end))
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    first_connexion = date_connexion[0]
    for i in range(len(date_connexion)):
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


def plot_connexion(ID, file):
    connexion_days = connexions_date(ID,file)
    X = np.arange(len(connexion_days))
    plt.plot(X,connexion_days, color='turquoise')
    plt.ylabel("Number of connexions")
    plt.xlabel("Number of days")
    # plt.title("Number of connexions per day since first connexion of {}".format(ID))
    plt.show()


def number_activities_connexion(ID, file):
    '''
    :param ID:
    :param file:
    :return: a list of list such that len(list) = number of connexions and list[i] = number of activities of connexion [i]
    '''
    with open(file) as json_data:
        data = json.load(json_data)
        es = data["es"]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                debut = es[event]["date"]
                end = debut + es[event]["data"]["duration"]
                date_activities_completed.append((debut,end))
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities = len(date_activities_completed)
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    first_connexion = date_connexion[0]
    for i in range(len(date_connexion)):
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


def frequency_activity(ID, data):
    '''
    :param ID:
    :param data:
    :return:
    '''
    with open(data) as json_data:
        data = json.load(json_data)
        es = data["es"]




def number_activity_per_connexion(ID, file_path):
    '''
    :param ID: user_key
    :param file: file with data
    :return:
    '''
    with open(file_path) as json_data:
         data = json.load(json_data)
         es = data["es"]
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
    #print(date_activities_completed)
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


def number_activity_per_connexion_global(file_path):
    '''
    :param file_path: file with data
    :return: plot a histogram
    '''
    with open(file_path) as json_data:
        data = json.load(json_data)
        su = data["su"]
    nb_activity = []
    for ID in su.keys():
        nb = number_activity_per_connexion(ID,file_path)
        nb_activity.append(nb)
    plt.title("Nombre d'activités par connexion", fontsize=10)
    plt.xlabel("Nombre d'activités")
    plt.ylabel("Nombre d'utilisateurs")
    plt.hist(nb_activity)
    plt.show()

