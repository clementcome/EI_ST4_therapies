import json


def list_activities(file="data/des.json"):
    with open(file) as input_file:
        data = json.load(input_file)
    d_activities = {}
    count_error = 0
    for key in data.keys():
        try:
            activity = data[key]["data"]["activity"]
            if activity in d_activities.keys():
                d_activities[activity] += 1
            else:
                d_activities[activity] = 1
        except KeyError:
            count_error +=1
    return d_activities, count_error

def get_1_acouphenometry(file="data/des.json"):
    with open(file) as input_file:
        data = json.load(input_file)
    for key in data.keys():
        try:
            activity = data[key]["data"]["activity"]
            if activity == "acouphenometry":
                return data[key]
        except:
            pass