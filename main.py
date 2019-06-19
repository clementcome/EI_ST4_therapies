from project.explore import list_activities, get_1_acouphenometry, get_trajectories_acouphenometry
from project.visu import display_1_acouphenometry, display_trajectory, display_therapy
from project.visu import display_therapy_used, display_therapy_per_user_3d, display_corr_activities
from project.visu import programs_status, display_corr_principal_users
from project.extract import extract_activity_data
from project.activity_analysis import therapy_analysis
from project.cluster import pca_kmeans_activities, pca_therapy_activities, pca_kmeans_users, tsne_kmeans_users


# d_activities, count_error = list_activities()

# print(d_activities,count_error)

# data_acouphenometry = get_1_acouphenometry()
# print(data_acouphenometry["data"].keys())

# display_1_acouphenometry()

# get_trajectories_acouphenometry()

# display_trajectory(200)
# extract_activity_data()

# therapy_analysis()
# display_therapy(5)
# display_therapy_used()
# display_therapy_per_user_3d()

# display_corr_activities()
# pca_kmeans_activities()
# pca_therapy_activities()

# display_corr_principal_users()
# pca_kmeans_users()
# tsne_kmeans_users()

# programs_status()


from dash_app import app_therapy,app_activity

# app_therapy.run_server(debug=True)
app_activity.run_server(debug=True)