import pandas as pd
import json
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np

from project.activity_analysis import therapy_from_activity
from project.extract import dataframe_activity_frequency

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, OPTICS
from sklearn.manifold import TSNE
from sklearn.metrics import davies_bouldin_score, silhouette_score

def pca_kmeans_activities(therapy_filepath="data/therapyByUser.json"):
    df = dataframe_activity_frequency()
    df = df.transpose()
    # print(df)
    # print(df.describe())
    pca = PCA(n_components=2)
    pca.fit(df)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    activity_2 = pca.transform(df)
    kmeans = KMeans(n_clusters=3).fit(activity_2)
    labels = kmeans.labels_
    activity_2 = pd.DataFrame({"PCA1":activity_2[:,0], "PCA2":activity_2[:,1],
            "labels":labels},
        index=df.index)
    # print(activity_2)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        text=activity_2[activity_2["labels"] == label].index, name=str(label), marker={"size":15} ) for label in activity_2["labels"].unique()]
    layout = go.Layout(
        xaxis={"title":"PC1 {}% of explained variance".format(str(pca.explained_variance_ratio_[0])[2:4])},
        yaxis={"title":"PC2 {}%".format(str(pca.explained_variance_ratio_[1])[2:4])})
    py.plot({"data":data,"layout":layout})

def pca_therapy_activities(therapy_filepath="data/therapyByUser.json"):
    therapy_activity = therapy_from_activity()
    df = dataframe_activity_frequency()
    df = df.transpose()
    index = df.index
    # print(df.describe())
    pca = PCA(n_components=2)
    pca.fit(df)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    activity_2 = pca.transform(df)
    activity_2 = pd.DataFrame({"PCA1":activity_2[:,0], "PCA2":activity_2[:,1],
            "labels":[therapy_activity[activity] for activity in df.index]},
        index=index)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        name=str(label), marker={"size":15}, text=activity_2[activity_2["labels"] == label].index ) for label in activity_2["labels"].unique()]
    py.plot(data)

def pca_kmeans_users(frequency_filepath="data/data_frequency.json"):
    df_freq = dataframe_activity_frequency()
    # print(df_freq.head())
    pca = PCA(n_components=2)
    pca.fit(df_freq)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    users_2 = pca.transform(df_freq)
    # data = [go.Scatter(
    #     x=users_2[:,0],
    #     y=users_2[:,1],
    #     mode = "markers"
    # )]
    kmeans = KMeans(n_clusters=3).fit(df_freq)  
    labels = kmeans.labels_
    activity_2 = pd.DataFrame({"PCA1":users_2[:,0], "PCA2":users_2[:,1],
            "labels":labels},
        index=df_freq.index)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        text=df_freq.index, name=str(label), marker={"size":15} ) 
        for label in np.sort(activity_2["labels"].unique())]
    layout = go.Layout(
        xaxis={"title":"PC1 {}% of explained variance".format(str(pca.explained_variance_ratio_[0])[2:4])},
        yaxis={"title":"PC2 {}%".format(str(pca.explained_variance_ratio_[1])[2:4])},)
    py.plot({"data":data,"layout":layout})

def tsne_kmeans_users(frequency_filepath="data/data_frequency.json"):
    df_freq = dataframe_activity_frequency()
    # print(df_freq.head())
    tsne = TSNE(n_components=2)
    users_2 = tsne.fit_transform(df_freq)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    # data = [go.Scatter(
    #     x=users_2[:,0],
    #     y=users_2[:,1],
    #     mode = "markers"
    # )]
    kmeans = KMeans(n_clusters=2).fit(df_freq)
    labels = kmeans.labels_
    activity_2 = pd.DataFrame({"PCA1":users_2[:,0], "PCA2":users_2[:,1],
            "labels":labels},
        index=df_freq.index)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        text=df_freq.index, name=str(label) ) for label in activity_2["labels"].unique()]
    py.plot(data)