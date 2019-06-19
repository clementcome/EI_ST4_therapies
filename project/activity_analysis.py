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
            else :
                upper_bound += 3600*24
                index_day += 1
            index_activity += 1
    return number_connexion_days

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
    therapy_activity = therapy_from_activity()
    therapies = set(therapy_activity.values())
    data_user = {}      # a first dictionary to get all the activities done by a user
    data_therapy = {}
    events_by_uuid = {}
    for eventKey in es:
        event = es[eventKey]
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




