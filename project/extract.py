import json
import pandas as pd

def extract_activity_data(des_path="data/des.json",dsu_path="data/dsu.json",ouput_path="data/data_activity.json"):
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
        if "data" in d_events[eventKey].keys():
            if "score" in d_events[eventKey]["data"].keys():
                d_es[eventKey]["data"]["score"] = d_events[eventKey]["data"]["score"]
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

def dataframe_from_therapy(therapy_path="data/therapyByUser.json"):
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

def frequencies_from_dataframe(df):
    """
    Return frequencies associated to each activity and user
    returns dict: keys are row indices and values are median frequencies
    """
    changes = detect_change_activity(df)
    d_frequency = {}
    for i in range(len(changes)-1):
        start, end = changes[i], changes[i+1]-1
        if end - start > 1:
            time_sorted = df["time"].iloc[start:end].sort_values(ascending=False)
            time_sorted = list(time_sorted)
            time_differencies = [(time_sorted[i]-time_sorted[i+1]) for i in range(len(time_sorted)-1)]
            time_differencies.sort()
            median = time_differencies[len(time_differencies) // 2]
            d_frequency[start]= median/86400
    return d_frequency

def use_frequencies(df=dataframe_from_therapy(),ouput_path="data/data_frequency.json"):
    """
    Return a dataframe with giving frequencies by activity, therapy and user
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
