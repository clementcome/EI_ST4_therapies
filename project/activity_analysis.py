import json


def mean_time_between_two_connexions(ID,data):
    '''
    :param ID: user_key
    :param data: file with data
    :return: number of connexions of the user
    '''
    with open(data) as json_data:
        data = json.load(json_data)
        es = data["es"]
       # su = data["su"]
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



def connexions_date(ID,data):
    '''
    :param ID: user_key
    :param data: file with data
    :return: list with data time
    '''
    with open(data) as json_data:
        data = json.load(json_data)
        es = data["es"]
    date_activities_completed = []
    for event in es:
        if es[event]["userKey"] == ID :
            if es[event]["type"] == "ACTIVITY_COMPLETE" :
                debut = es[event]["type"]["date"]
                end = debut + es[event]["type"]["data"]["duration"]
                date_activities_completed.append((debut,end))
    date_activities_completed.sort()
    date_connexion = [date_activities_completed[0][0]]
    number_activities : len(date_activities_completed)
    for i in range(number_activities-1):
        if date_activities_completed[i+1][0] - date_activities_completed[i][1] >= 900 :
            date_connexion.append(date_activities_completed[i+1][0])
    first_connexion = date_connexion[0]
    for time in date_connexion:
        time -= first_connexion
    number_of_days = date_connexion[-1]//(3600*24)
    number_connexion_days = [0]*number_of_days
    index_day = 0
    index_activity = 0
    upper_bound = 3600*24
    while index_day < number_of_days:
        while index_activity < number_activities:
            if date_activities_completed[index_activity] < upper_bound :
                number_connexion_days[i] += 1
            elif :
                upper_bound += 3600*24
                index_day += 1
            index_activity += 1
    return number_connexion_days









