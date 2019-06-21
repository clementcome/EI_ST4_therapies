import json
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date


def get_trajectories_acouphenometry(file="data/des.json"):
    """
    Saves all the trajectories of acouphenometry from event sourcing
    in a file named dtrajectories.json
    """
    with open(file) as input_file:
        data =json.load(input_file)
    d_trajectories = {}
    for key in data.keys():
        try:
            activity = data[key]["data"]["activity"]
            if activity == "acouphenometry":
                d_trajectories[data[key]["userKey"]] = data[key]["data"]["points"]
        except:
            pass
    with open("data/dtrajectories.json","w") as output_file:
        json.dump(d_trajectories,output_file)

def extract_activity_data(des_path="data/des.json",
    dsu_path="data/dsu.json",
    ouput_path="data/data_activity.json"):
    """
    Script to extract our interesting data from event sourcing and strong users
    Dumps dictionary into output_path
    Dictionary structure is : {"su":{userKey:{"reducers":{"user":{subscriptionDate}}}},
        "es":{eventKey:{"score":,
            "data":{"activity":activity,"duration":duration,"gameScore":gameScore,"uuid":uuid,"referrer":referrer}}}}
    """
    d_activity = {}
    with open(dsu_path) as input_file:
        d_users = json.load(input_file)
    with open(des_path) as input_file:
        d_events = json.load(input_file)
    d_su = {}
    for userKey in d_users:
        try:
            d_su[userKey] = {"reducers":
                {"user":
                    {"subscriptionDate":
                        d_users[userKey]["reducers"]["user"]["subscriptionDate"]
                    }
                }
            } 
        except:
            pass

    d_es = {
        eventKey:{
            "type": d_events[eventKey]["type"],
            "date": d_events[eventKey]["date"],
            "userKey": d_events[eventKey]["userKey"],
            "data":{}
        }
    for eventKey in d_events}

    for eventKey in d_events:
        if "score" in d_events[eventKey].keys():
            d_es[eventKey]["score"] = d_events[eventKey]["score"]
        if "data" in d_events[eventKey].keys():
            if "activity" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["activity"] = d_events[eventKey]["data"]["activity"]
            if "duration" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["duration"] = d_events[eventKey]["data"]["duration"]
            if "gameScore" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["gameScore"] = d_events[eventKey]["data"]["gameScore"]
            if "uuid" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["uuid"] = d_events[eventKey]["data"]["uuid"]
            if "referrer" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["referrer"] = d_events[eventKey]["data"]["referrer"]
    d_activity = {"su":d_su,"es":d_es}
    with open(ouput_path,'w') as output_file:
        json.dump(d_activity,output_file)


def therapy_from_activity(activities_path = "data/activities.json"):
    """
    Returns a dictionary with activity as keys and therapy as values
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


def dataframe_from_therapy(therapy_path="data/therapyByUser.json"):
    """
    Returns a pandas DataFrame with user, therapy, activity and time as columns
    """
    d_therapy = json.load(open("data/therapyByUser.json"))
    data_activity = {"user":[],"therapy":[],"activity":[],"time":[]}
    for userKey in d_therapy:
        user = d_therapy[userKey]
        for therapyKey in user:
            therapy = user[therapyKey]
            for activityKey in therapy:
                activity = therapy[activityKey]
                for time in activity:
                    data_activity["user"].append(userKey)
                    data_activity["therapy"].append(therapyKey)
                    data_activity["activity"].append(activityKey)
                    data_activity["time"].append(time)
    df = pd.DataFrame(data_activity)
    return df

def detect_change_activity(df):
    """
    Detect each change of activity in the dataframe listing every activity done by every user
    ordered by user, therapy, activity
    """
    resu = [0]
    n = df.shape[0]
    for i in range(n-1):
        row = df.iloc[[i]]
        next_row = df.iloc[[i+1]]
        if row["user"].values != next_row["user"].values:
            resu.append(i+1)
        elif row["activity"].values != next_row["activity"].values:
            resu.append(i+1)
    if resu[-1] != n:
        resu.append(n)
    return resu

def dict_days_activity(timestamps):
    """
    For an activity, given its timestamps: it returns for each day how many times
    the user did this activity
    """
    d = {}
    for timestamp in timestamps:
        date = datetime.fromtimestamp(timestamp).date()
        if date in d.keys():
            d[date] += 1
        else:
            d[date] = 1
    return d

def frequencies_from_dataframe(df):
    """
    Returns frequencies associated to each activity and user difference with the previous one is
    we count for each day how many times a user did each activity
    returns dict: keys are row indices and values are median frequencies
    """
    changes = detect_change_activity(df)
    d_frequency = {}
    for i in range(len(changes)-1):
        start, end = changes[i], changes[i+1]-1
        timestamps = df["time"].iloc[start:end]
        d_days = dict_days_activity(timestamps)
        try:
            # max_day = max(d_days.keys())
            max_day = date(2019,6,14)
            min_day = min(d_days.keys())
            if max_day != min_day:
                mean = sum(d_days.values())/(max_day-min_day).days
                d_frequency[start]= mean
        except:
            pass
    return d_frequency

def use_frequencies(df= dataframe_from_therapy(),ouput_path="data/data_frequency.json"):
    """
    Returns a dataframe giving frequencies by activity, therapy and user
    """
    d_frequency_row = frequencies_from_dataframe(df)
    d_frequency = {"user":[],"therapy":[],"activity":[],"frequency":[]}
    for row_id in d_frequency_row:
        row = df.iloc[[row_id]]
        d_frequency["user"].append(row["user"].values[0])
        d_frequency["therapy"].append(row["therapy"].values[0])
        d_frequency["activity"].append(row["activity"].values[0])
        d_frequency["frequency"].append(d_frequency_row[row_id])
    with open(ouput_path,'w') as output_file:
        json.dump(d_frequency, output_file)
    df_frequency = pd.DataFrame(d_frequency)
    return df_frequency

def dataframe_activity_frequency(frequency_path="data/data_frequency.json"):
    """
    Returns a dataframe with userKey as indices and name of activities as columns
    """
    d_freq = json.load(open(frequency_path))
    d_activity = {}
    users = d_freq["user"]
    activities = d_freq["activity"]
    frequencies = d_freq["frequency"]
    for i in range(len(users)):
        user = users[i]
        activity = activities[i]
        frequency = frequencies[i]
        if user in d_activity.keys():
            d_activity[user][activity] = frequency
        else:
            d_activity[user] = {activity: frequency}
    df_freq = pd.DataFrame(d_activity).transpose()
    cols_to_keep = []
    for col in df_freq.columns:
        if df_freq[col].count()>150:
            cols_to_keep.append(col)
    df_freq = df_freq[cols_to_keep]
    df_freq = df_freq.dropna()
    return df_freq