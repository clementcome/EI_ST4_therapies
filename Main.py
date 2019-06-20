from project.explore import list_activities, get_1_acouphenometry, get_trajectories_acouphenometry
from project.visu import display_1_acouphenometry, display_trajectory
from project.extract import extract_activity_data

from project.activity_analysis import connexions_date
from project.activity_analysis import mean_time_between_connexions
from project.activity_analysis import plot_connexion
from project.activity_analysis import mean_time_connexions
from project.activity_analysis import number_activity_per_connexion
from project.activity_analysis import mean_time_between_connexions_global

from project.second_analysis import number_of_connexions_per_day
from project.second_analysis import plot_connexion
from project.second_analysis import number_of_connexions_per_day_global
from project.second_analysis import plot_connexion_global
from project.second_analysis import plot_time_between_connexion
from project.second_analysis import plot_time_between_connexion_global
from project.second_analysis import plot_number_activities_per_connexion_global
from project.second_analysis import number_activities_per_connexion


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
# mean_time_between_connexions_global(data)



# plot_connexion_global(data)
# plot_time_between_connexion(ID, data)
# plot_time_between_connexion_global(data)
plot_number_activities_per_connexion_global(data)
# print(number_activities_per_connexion(ID, data))
