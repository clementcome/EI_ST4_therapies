import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go

from project.explore import get_1_acouphenometry
from project.activity_analysis import therapy_from_activity

def display_1_acouphenometry():
    data_acouphenometry = get_1_acouphenometry()
    points = data_acouphenometry["data"]["points"]
    f = [point["f"] for point in points]
    q = [point["q"] for point in points]
    plt.plot(q,f)
    plt.scatter(q[-1],f[-1],c="red",s=100)
    plt.xlim(1,0)
    plt.ylim(0,1)
    plt.axis("equal")
    plt.show()

def display_trajectory(i=1,file = "data/dtrajectories.json"):
    """
    To execute this function you must have executed get_trajectories_acouphenometry once before.
    """
    with open(file) as input_file:
        trajectories = json.load(input_file)
    keys = trajectories.keys()
    key = list(keys)[i]
    points = trajectories[key]
    f = [point["f"] for point in points]
    q = [point["q"] for point in points]
    plt.plot(q,f)
    plt.scatter(q[-1],f[-1],c="red",s=100)
    plt.xlim(1,0)
    plt.ylim(0,1)
    plt.show()

def display_therapy(i=0, therapy_path = "data/therapyByUser.json"):
    with open(therapy_path) as input_file:
        d_therapy = json.load(input_file)
    user = list(d_therapy.keys())[i]
    activity_user = {"therapy":[],"activity":[],"count":[]}
    for therapy in d_therapy[user]:
        for activity in d_therapy[user][therapy]:
            activity_user["therapy"].append(therapy)
            activity_user["activity"].append(activity)
            activity_user["count"].append(len(d_therapy[user][therapy][activity]))
    df_acti = pd.DataFrame(activity_user)
    data = [go.Bar(x=df_acti[df_acti["therapy"]==therapy]["activity"],
    y=df_acti[df_acti["therapy"]==therapy]["count"],
    name = therapy) for therapy in df_acti["therapy"].unique()]
    py.plot(data)

def display_therapy_used(therapy_path = "data/therapyByUser.json"):
    with open(therapy_path) as input_file:
        d_therapy = json.load(input_file)
    activity_therapy = therapy_from_activity()
    therapy_activity = {}
    for activity in activity_therapy:
        therapy = activity_therapy[activity]
        if therapy in therapy_activity.keys():
            therapy_activity[therapy].append(activity)
        else:
            therapy_activity[therapy] = [activity]
    therapies = therapy_activity.keys()
    d_count = {activity:0 for activity in activity_therapy.keys()}
    for user in d_therapy:
        d_user = d_therapy[user]
        for therapy in d_user:
            d_therapy_user = d_user[therapy]
            for activity in d_therapy_user:
                if activity in d_count.keys():
                    d_count[activity] += len(d_therapy_user[activity])
                else:
                    d_count[activity] = len(d_therapy_user[activity])
    data = []
    for therapy in therapies:
        x = therapy_activity[therapy]
        y = [d_count[activity] for activity in x]
        trace = go.Bar(x=x,y=y,name=therapy)
        data.append(trace)
    py.plot(data)

def display_therapy_per_user_3d(therapy_filepath="data/therapyByUser.json"):
    therapies = ["trt","cbt","relaxation"]
    with open(therapy_filepath) as input_file:
        d_therapy = json.load(input_file)
    d_count = {
        user: {
            therapy: sum([ len(d_therapy[user][therapy][activity]) 
                            for activity in d_therapy[user][therapy] ])
        for therapy in d_therapy[user]}
    for user in d_therapy}
    x = [d_count[user][therapies[0]] for user in d_count]
    y = [d_count[user][therapies[1]] for user in d_count]
    z = [d_count[user][therapies[2]] for user in d_count]
    data = [
        go.Scatter3d(x=x,y=y,z=z,mode="markers")
    ]
    layout = go.Layout(scene={
        "xaxis":{"title":therapies[1],"type":"log"},
        "yaxis":{"title":therapies[2],"type":"log"},
        "zaxis":{"title":therapies[0],"type":"log"},
        "aspectmode":"cube"
    })
    py.plot({"data":data,"layout":layout})