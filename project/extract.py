import json

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
    