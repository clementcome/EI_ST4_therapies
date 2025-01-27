import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go

from project.explore import get_1_acouphenometry
from project.extract import therapy_from_activity
from project.extract import dataframe_activity_frequency

def display_1_acouphenometry():
    """
    DEPRECATED
    Display the trajectory of the first acouphenometry in event sourcing
    """
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
    """
    Display the use of activities (number of activities completed) for a user given by its line number
    Colors the bars depending on their therapy
    """
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
    """
    Display the use of activities (number of activities completed) for every user given by its line number
    Colors the bars depending on their therapy
    """
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
    layout = go.Layout(xaxis={"tickfont":{"size":15}},height=600)
    py.plot({"data":data,"layout":layout})

def display_therapy_per_user_3d(therapy_filepath="data/therapyByUser.json"):
    """
    Display the use of therapies for every user in 3D
    """
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

def display_corr_activities(frequency_path="data/data_frequency.json"):
    """
    Display the correlation matrix of activities described by users' use-frequency
    """
    df = dataframe_activity_frequency()
    corr = df.corr()
    # corr.style.background_gradient(cmap="coolwarm",axis=None)
    data = [go.Heatmap(z=corr,x=corr.columns,y=corr.index)]
    py.plot(data)

def display_corr_principal_users(frequency_path="data/data_frequency.json"):
    """
    Display the correlation matrix of users described by activities' use-frequency
    """
    df = dataframe_activity_frequency().transpose()
    corr = df.corr()
    # corr.style.background_gradient(cmap="coolwarm",axis=None)
    data = [go.Heatmap(z=corr,x=corr.columns,y=corr.index)]
    layout = go.Layout(xaxis={"showticklabels":False},yaxis={"showticklabels":False},
        width=700,height=700)
    py.plot({"data":data,"layout":layout})

#des[type] = “PROGRAM_” + START, CANCEL, COMPLETE + (des[data][referrer][program] + des[data][referrer][type] where des[type] = “ACTIVITY_START”)
def programs_status(file="data/des.json"):
    """
    Display the proportion of program started completed and cancelled for every program
    """
    with open(file) as input_file:
        data = json.load(input_file)
    comptage={}
    programmes = ["improveMood", "reduceStress", "improveConcentration", "improveSleep"]
    types = ['PROGRAM_START', 'PROGRAM_CANCEL', 'PROGRAM_COMPLETE']
    comptage['PROGRAM_START'] = {}
    comptage['PROGRAM_CANCEL'] = {}
    comptage['PROGRAM_COMPLETE'] = {}

    for programme in programmes :
        comptage['PROGRAM_START'][programme]=0
        comptage['PROGRAM_CANCEL'][programme]=0
        comptage['PROGRAM_COMPLETE'][programme]=0

    for utilisateur in data.keys():
        #print(data[utilisateur])
        try:
            prog = data[utilisateur]["data"]["program"]
            type = data[utilisateur]["type"]
            if type in types and prog in programmes:
                comptage[type][prog] += 1

        except KeyError:
            pass
    valStart = [comptage['PROGRAM_START'][i] for i in programmes]
    valCancel = [comptage['PROGRAM_CANCEL'][i] for i in programmes]
    valComplete = [comptage['PROGRAM_COMPLETE'][i] for i in programmes]

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(4)
    bar_width = 0.25
    opacity = 0.8

    rects1 = plt.bar(index, valStart, bar_width,
    alpha=opacity,
    color='b',
    label='START')

    rects2 = plt.bar(index + bar_width, valCancel, bar_width,
    alpha=opacity,
    color='g',
    label='CANCEL')

    rects3 = plt.bar(index + bar_width*2, valComplete, bar_width,
    alpha=opacity,
    color='r',
    label='COMPLETE')

    plt.ylabel('Nombre d'+"'"+'utilisateurs')
    plt.xticks(index + bar_width, ('Improve Mood', 'Reduce Stress', 'Improve Concentration', 'Improve Sleep'))
    plt.legend()

    plt.tight_layout()
    plt.show()