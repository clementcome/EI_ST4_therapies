import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from project.explore import get_1_acouphenometry

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
    colors = {"trt":"#ff0000",
    "cbt":"#fffa00",
    "relaxation":"#00ff0c",
    "residualInhibition":"#00ffe5",
    "knowledge":"#0015ff",
    "questionnaire":"#ff00f6"}
    color_serie = [colors[therapy] for therapy in df_acti["therapy"]]
    plt.bar(df_acti["activity"],df_acti["count"],color=color_serie)
    plt.show()