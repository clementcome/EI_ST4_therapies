import pandas as pd
import json
import plotly.offline as py
import plotly.graph_objs as go

from project.activity_analysis import therapy_from_activity
from project.extract import dataframe_activity_frequency

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

def pca_kmeans_activities(therapy_filepath="data/therapyByUser.json"):
    df = dataframe_activity_frequency()
    df = df.transpose()
    print(df)
    # print(df.describe())
    pca = PCA(n_components=2)
    pca.fit(df)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    activity_2 = pca.transform(df)
    kmeans = KMeans(n_clusters=1).fit(activity_2)
    labels = kmeans.labels_
    activity_2 = pd.DataFrame({"PCA1":activity_2[:,0], "PCA2":activity_2[:,1],
            "labels":labels},
        index=df.index)
    print(activity_2)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        text=activity_2.index, name=str(label), marker={"size":15} ) for label in activity_2["labels"].unique()]
    layout = go.Layout(
        xaxis={"title":"PC1 {}% of explained variance".format(str(pca.explained_variance_ratio_[0])[2:4])},
        yaxis={"title":"PC2 {}%".format(str(pca.explained_variance_ratio_[1])[2:4])})
    py.plot({"data":data,"layout":layout})

def pca_therapy_activities(therapy_filepath="data/therapyByUser.json"):
    d_therapy = json.load(open(therapy_filepath))
    d_count = {}
    therapy_activity = therapy_from_activity()
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
    df= df[cols_to_keep]
    df = df.dropna().transpose()
    # print(df.describe())
    pca = PCA(n_components=2)
    pca.fit(df)
    # print(pca.components_)
    # print(pca.explained_variance_ratio_)
    activity_2 = pca.transform(df)
    activity_2_therapy = pd.DataFrame({"PCA1":activity_2[:,0], "PCA2":activity_2[:,1],
            "therapy":[therapy_activity[activity] for activity in df.index]},
        index=df.index)
    data = [go.Scatter(x=activity_2_therapy[activity_2_therapy["therapy"] == therapy]["PCA1"],
        y=activity_2_therapy[activity_2_therapy["therapy"] == therapy]["PCA2"],mode="markers",
        text=df.index, name=therapy ) for therapy in activity_2_therapy["therapy"].unique()]
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
        text=df_freq.index, name=str(label), marker={"size":15} ) for label in activity_2["labels"].unique()]
    layout = go.Layout(
        xaxis={"title":"PC1 {}% of explained variance".format(str(pca.explained_variance_ratio_[0])[2:4])},
        yaxis={"title":"PC2 {}%".format(str(pca.explained_variance_ratio_[1])[2:4])})
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
    kmeans = KMeans(n_clusters=1).fit(df_freq)
    labels = kmeans.labels_
    activity_2 = pd.DataFrame({"PCA1":users_2[:,0], "PCA2":users_2[:,1],
            "labels":labels},
        index=df_freq.index)
    data = [go.Scatter(x=activity_2[activity_2["labels"] == label]["PCA1"],
        y=activity_2[activity_2["labels"] == label]["PCA2"],mode="markers",
        text=df_freq.index, name=str(label) ) for label in activity_2["labels"].unique()]
    py.plot(data)