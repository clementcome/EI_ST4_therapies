import pandas as pd
import json
import plotly.offline as py
import plotly.graph_objs as go

from project.activity_analysis import therapy_from_activity

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def pca_kmeans_activities(therapy_filepath="data/therapyByUser.json"):
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
    kmeans = KMeans(n_clusters=4).fit(activity_2)
    labels = kmeans.labels_
    # labels = [therapy_activity[activity] for activity in df.index]

    data = [go.Scatter(x=activity_2[:,0],y=activity_2[:,1],mode="markers",
        text=df.index, marker={"color":labels,"colorscale":"Rainbow"}, )]
    py.plot(data)