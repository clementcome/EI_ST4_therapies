"""
Visualize the use of activities :
Compare for 2 activities the frequency of use of all users
"""

import json
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from project.extract import dataframe_from_therapy, use_frequencies

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_activity = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df_frequency = pd.DataFrame(json.load(open("data/data_frequency.json")))

activities = {
    "theIsland":"L'ile",
    "constellations":"Constellations",
    "simons":"Simons",
    "intoTheWind":"Contre vent",
    "associationSort":"Tri à thème",
    "lostRecipe":"Recette perdue",
    "toyFactory":"L'usine à jouet",
    "coherentBreathing":"Cohérence cardiaque",
    "lullaby":"Berceuse",
    "squareBreathing":"Respiration recette",
    "abdominalBreathing":"Respiration abdominale",
    "keepTheShape":"Garde la forme",
    "smoothieBar":"Smoothie bar",
    "diapason":"Présentation diapason",
    "auditorySystem":"Système auditif",
    "neurophysiologicModel":"Modèle neurophysiologique",
    "tinnitusMechanisms":"Mécanismes des acouphènes",
    "automaticThoughts":"Pensées automatiques",
    "professionnals":"Médecin référent",
    "tfi":"TFI",
    "thi":"THI",
    "isi":"ISI",
    "hads":"HADS",
    "residualInhibitionDiagnosis":"Test de l'IR",
    "acouphenometry":"Acouphenometry",
}

app_activity.layout = html.Div([
    html.Div(html.H1("Activity use"),
        style = {"textAlign":"center","padding-bottom":"10","padding-top":"10"}),
    html.Div([
        html.Div(dcc.Dropdown(id="select-xaxis",
            options=[{"value":i,"label":activities[i]} for i in activities],
            value = "theIsland"),
        className= "four columns",
        style={"display": "block", "margin-left": "auto",
            "margin-right": "auto", "width": "50%"}),
        html.Div(dcc.Dropdown(id="select-yaxis",
            options=[{"value":i,"label":activities[i]} for i in activities],
            value = "constellations"),
        className= "four columns",
        style={"display": "block", "margin-left": "auto",
            "margin-right": "auto", "width": "50%"}),
    ],  className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
            "margin-right": "auto", "width": "80%"}),
    html.Div(dcc.Checklist(id="log-scale",
        options= [
            {'label':'Logarithmic scale','value':'log'}
        ],
        values = ['log']
    ),  className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
            "margin-right": "auto", "width": "80%"}),
    html.Div(dcc.Graph(id="my-graph"))
], className="container")

@app_activity.callback(
    Output("my-graph","figure"),
    [
        Input("select-xaxis","value"),
        Input("select-yaxis","value"),
        Input("log-scale","values")
    ]
)
def update_graph(selected_x,selected_y,scale_values):
    x = df_frequency[df_frequency["activity"] == selected_x]["frequency"]
    y = df_frequency[df_frequency["activity"] == selected_y]["frequency"]

    droite = go.Scatter(x=[0,3],y=[0,3],mode="lines")
    # for user in d_count:
    #     if (selected_x in d_count[user].keys()) and (selected_y in d_count[user].keys()):
    #         x.append(d_count[user][selected_x])
    #         y.append(d_count[user][selected_y])

    data = [go.Scatter(x=x,y=y,mode="markers"),droite]
    layout = go.Layout(height=700,xaxis={"title":activities[selected_x]},
        yaxis={"title":activities[selected_y], "scaleanchor":"x"})
    if "log" in scale_values:
        layout.yaxis.type = "log"
        layout.xaxis.type = "log"
    return {"data":data, "layout":layout}