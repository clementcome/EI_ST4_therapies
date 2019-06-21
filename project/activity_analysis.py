import json
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


def mean_time_between_connexions(ID,file_path):
    '''
    :param ID: user_key
    :param file_path
    :return:
    '''
    with open(file_path) as json_data:
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


def mean_time_between_connexions_test(ID,file_path):
    '''
    :param ID: user_key
    :param file_path: file with data
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


def mean_time_connexions(file_path):
    '''
    :param file_path: file with data
    :return:
    '''
    with open(file_path) as json_data:
        data = json.load(json_data)
        su = data["su"]
    means = []
    for ID in su.keys():
        m = mean_time_between_connexions_test(ID,file_path)
        if m != 0 :
            means.append(m)
    X = np.arange(len(means))
    plt.plot(X,means, color = 'turquoise')
    plt.ylabel("Number of connexions")
    plt.xlabel("User")
    # plt.title("Number of connexions per day since first connexion of {}".format(ID))
    # Mettre de meilleurs noms de graphes
    plt.show()


def mean_time_between_connexions_global(file_path):
    '''
    :param file_path: file with data
    :return: plot a histogram
    '''
    with open(file_path) as json_data:
        data = json.load(json_data)
        su = data["su"]
    means = []
    for ID in su.keys():
        m = mean_time_between_connexions_test(ID,file_path)
        if m != 0 :
            means.append(m)
    plt.title('Fréquence de connexion inférieure au temps préconisé ', fontsize=10)
    plt.xlabel('Durée moyenne entre deux connexions')
    plt.ylabel("Nombre d'utilisateurs")
    plt.hist(means)
    plt.show()


def connexions_date(ID,file_path):
    '''
    :param ID: user_key
    :param file_path: file with data
    :return: list with data time
    '''
    with open(file_path) as json_data:
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

def therapy_from_activity(activities_path = "data/activities.json"):
    """
    Return a dictionary with activity as keys and therapy as values
    """
    with open(activities_path) as input_file:
        activities = json.load(input_file)
    d_therapy = {}
    for therapy in activities:
        for activity in activities[therapy]:
            d_therapy[activity["name"]] = therapy
    return d_therapy

def therapy_analysis(data_activity_path = "data/data_activity.json",
    activities_path = "data/activities.json",
    output_path = "data/therapyByUser.json"):
    """
    Create a json file with this format : {user:{therapyName:{activity:[date]}}}
    Keeps only the activities not done during the guided tour.
    """
    with open(data_activity_path) as data_activity_file:
        data_activity = json.load(data_activity_file)
    es = data_activity["es"]
    su = data_activity["su"]
    li_su = list(su.keys())
    therapy_activity = therapy_from_activity()
    therapies = set(therapy_activity.values())
    data_user = {}      # a first dictionary to get all the activities done by a user
    data_therapy = {}
    events_by_uuid = {}
    for eventKey in es:
        event = es[eventKey]
        if "userKey" in event.keys():
            if event["userKey"] not in li_su:
                continue
        if "type" in event.keys():
            if "ACTIVITY" in event["type"]:
                if "uuid" in event["data"].keys():
                    uuid = event["data"]["uuid"]
                    if uuid in events_by_uuid.keys():
                        events_by_uuid[uuid][event["type"]] = event
                    else:
                        events_by_uuid[uuid] = {event["type"]: event}
    for uuid in events_by_uuid:
        events = events_by_uuid[uuid]
        if "ACTIVITY_START" in events.keys():
            start_event = events["ACTIVITY_START"]
            if "referrer" in start_event["data"].keys():
                referrer = start_event["data"]["referrer"]
                if "name" in referrer.keys() and referrer["name"] == "guidedTour":
                    continue
                if "ACTIVITY_COMPLETE" in events.keys():
                    event = events["ACTIVITY_COMPLETE"]
                    if "userKey" in event.keys():
                        userKey = event["userKey"]
                        if "activity" in event["data"].keys():
                            acti = {"activity":event["data"]["activity"],"date":event["date"]}
                            if userKey in data_user.keys():
                                data_user[userKey].append(acti)
                            else:
                                data_user[userKey] = [acti]
    for user in data_user:
        data_therapy[user] = {therapy :{} for therapy in therapies}
        for acti in data_user[user]:
            acti_name = acti["activity"]
            acti_date = acti["date"]
            if acti_name in therapy_activity.keys():
                therapy = therapy_activity[acti_name]
                if acti_name in data_therapy[user][therapy].keys():
                    data_therapy[user][therapy][acti_name].append(acti_date)
                else:
                    data_therapy[user][therapy][acti_name] = [acti_date]
    with open(output_path,'w') as output_file:
        json.dump(data_therapy,output_file)
