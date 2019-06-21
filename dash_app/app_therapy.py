"""Visualize the use of therapies in 3D counting the number of activities in each
therapies for each user"""

import json
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_therapy = dash.Dash(__name__, external_stylesheets=external_stylesheets)

d_therapy = json.load(open("data/therapyByUser.json"))
d_count = {
    user: {
        therapy: sum([ len(d_therapy[user][therapy][activity]) 
                        for activity in d_therapy[user][therapy] ])
    for therapy in d_therapy[user]}
for user in d_therapy}
therapies = {
    "trt":"Thérapie sonore",
    "cbt":"Thérapie cognitive et comportementale",
    "relaxation":"Relaxation",
    "residualInhibition":"Inhibition résiduelle",
    "knowledge":"Connaissances",
    "questionnaire":"Questionnaire",
}

app_therapy.layout = html.Div([
    html.Div([html.H1("Use of therapies")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div(
        [html.Div(dcc.Dropdown(id="select-xaxis", 
                options=[{'label': therapies[i], 'value': i} for i in therapies],
                value='trt', ), 
            className="four columns",
            style={"display": "block", "margin-left": "auto",
                "margin-right": "auto", "width": "33%"}),
        html.Div(dcc.Dropdown(id="select-yaxis", 
                options=[{'label': therapies[i], 'value': i} for i in therapies],
                value='cbt', ), 
            className="four columns",
            style={"display": "block", "margin-left": "auto",
                "margin-right": "auto", "width": "33%"}),
        html.Div(dcc.Dropdown(id="select-zaxis", 
                options=[{'label': therapies[i], 'value': i} for i in therapies],
                value='relaxation', ), 
            className="four columns",
            style={"display": "block", "margin-left": "auto",
                "margin-right": "auto", "width": "33%"}),
        ], className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
                                    "margin-right": "auto", "width": "80%"}),
    html.Div([dcc.Graph(id="my-graph")])
], className="container")

@app_therapy.callback(
    Output("my-graph", "figure"),
    [
        Input("select-xaxis","value"),
        Input("select-yaxis","value"),
        Input("select-zaxis","value"),
    ]
)
def update_figure(selected_x,selected_y,selected_z):
    x = [d_count[user][selected_x] for user in d_count]
    y = [d_count[user][selected_y] for user in d_count]
    z = [d_count[user][selected_z] for user in d_count]

    layout = go.Layout(height=700,scene={
        "xaxis":{"title":therapies[selected_x],"type":"log"},
        "yaxis":{"title":therapies[selected_y],"type":"log"},
        "zaxis":{"title":therapies[selected_z],"type":"log"},
        "aspectmode":"cube",
    })
    return {"data":data, "layout":layout}