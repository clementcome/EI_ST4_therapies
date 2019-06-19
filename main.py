from project.explore import list_activities, get_1_acouphenometry, get_trajectories_acouphenometry
from project.visu import display_1_acouphenometry, display_trajectory
from project.extract import extract_activity_data
from project.activity_analysis import connexions_date
from project.activity_analysis import mean_time_between_connexions
from project.activity_analysis import plot_connexion
from project.activity_analysis import mean_time_connexions
from project.activity_analysis import number_activity_per_connexion
from project.activity_analysis import mean_time_between_connexions_global



# d_activities, count_error = list_activities()

# print(d_activities,count_error)

# data_acouphenometry = get_1_acouphenometry()
# print(data_acouphenometry["data"].keys())

# display_1_acouphenometry()

# get_trajectories_acouphenometry()

# display_trajectory(200)
# extract_activity_data()


ID = "02MzOJc3Tc3jXPrlmvaR8A"
data = 'data/data_activity.json'
# plot_connexion(ID, data)
# print(connexions_date(ID,data))
# print(mean_time_between_connexions(ID,data))
# mean_time_connexions(data)
# print(number_activity_per_connexion(ID, data))
mean_time_between_connexions_global(data)



