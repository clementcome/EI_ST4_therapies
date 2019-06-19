import json
import pandas as pd
import numpy as np
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

def display_corr_activities(therapy_filepath="data/therapyByUser.json"):
    d_therapy = json.load(open(therapy_filepath))
    d_count = {}
    for user in d_therapy:
        d_count[user] = {}
        for therapy in d_therapy[user]:
            for activity in d_therapy[user][therapy]:
                d_count[user][activity] = len(d_therapy[user][therapy][activity])
    df = pd.DataFrame(d_count).transpose()
    corr = df.corr()
    # corr.style.background_gradient(cmap="coolwarm",axis=None)
    data = [go.Heatmap(z=corr,x=corr.columns,y=corr.index)]
    py.plot(data)

def display_corr_principal_users(therapy_filepath="data/therapyByUser.json"):
    d_therapy = json.load(open(therapy_filepath))
    d_count = {}
    for user in d_therapy:
        d_count[user] = {}
        for therapy in d_therapy[user]:
            for activity in d_therapy[user][therapy]:
                d_count[user][activity] = len(d_therapy[user][therapy][activity])
    df = pd.DataFrame(d_count).transpose()
    cols_to_keep = []
    for col in df.columns:
        if df[col].count()>250:
            cols_to_keep.append(col)
    df= df[cols_to_keep].dropna().transpose()
    corr = df.corr()
    # corr.style.background_gradient(cmap="coolwarm",axis=None)
    data = [go.Heatmap(z=corr,x=corr.columns,y=corr.index)]
    py.plot(data)

#des[type] = “PROGRAM_” + START, CANCEL, COMPLETE + (des[data][referrer][program] + des[data][referrer][type] where des[type] = “ACTIVITY_START”)
def programs_status(file="data/des.json"):
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

   plt.xlabel('Programme')
   plt.ylabel('Nombre d'+"'"+'utilisateurs')
   plt.title('Utilisation des programmes')
   plt.xticks(index + bar_width, ('improveMood', 'reduceStress', 'improveConcentration', 'improveSleep'))
   plt.legend()

   plt.tight_layout()
   plt.show()