from project.explore import list_activities, get_1_acouphenometry, get_trajectories_acouphenometry
from project.visu import display_1_acouphenometry, display_trajectory
from project.extract import extract_activity_data
from project.activity_analysis import therapy_analysis
from project.scores_successifs import score
# d_activities, count_error = list_activities()
from project.explore import list_activities, get_1_acouphenometry, list_activities_one_user,freq_keepTheShape, plot_two_activities, plot_all_activities, plot_diag
d_activities, count_error = list_activities()

# print(d_activities,count_error)
import seaborn as sns

import matplotlib.pyplot as  plt

'''
print(d_activities,count_error)
data_acouphenometry = get_1_acouphenometry()
print(data_acouphenometry)'''


'''
d_activities, count_error = list_activities_one_user()

print(d_activities,count_error)
'''
'''
freq_keepTheShape()
plt.show()'''


'''
plt.scatter(plot_two_activities()[0],plot_two_activities()[1])
plt.plot([0,200],[0,200], color="red")
plt.xscale('log')
plt.yscale('log')
print(plot_two_activities()[0],plot_two_activities()[1])
plt.show()'''

#
# matrixplot=sns.pairplot(plot_all_activities())
# #diagplot=sns.pairplot(plot_diag())
#
#
# plt.plot([0,200],[0,200], color="red")
# for i in range(0, len(matrixplot.axes)):
#             for j in range(0, len(matrixplot.axes)):
#                 matrixplot.axes[i,j].set(xscale='log', yscale='log')   #, xlim=(1,200), ylim=(1,200))
#
# #plt.savefig("/Users/maximeculot/Downloads/figure.png",dpi=500)
# plt.savefig("/Users/maximeculot/Downloads/figure.png")


#diagplot=sns.pairplot(plot_diag())
# for i in range(0,len(diagplot.axes)):
#     for j in range(0,len(diagplot.axes)):
#         diagplot.axes[i,j].set
#plt.show()

# data_acouphenometry = get_1_acouphenometry()
# print(data_acouphenometry["data"].keys())

# display_1_acouphenometry()

# get_trajectories_acouphenometry()

# display_trajectory(200)
extract_activity_data()

#therapy_analysis()

print (score())
