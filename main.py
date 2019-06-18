from project.explore import list_activities, get_1_acouphenometry, list_activities_one_user,freq_keepTheShape, plot_two_activities, plot_all_activities
d_activities, count_error = list_activities()

import seaborn as sns

import matplotlib.pyplot as  plt

'''
print(d_activities,count_error)
data_acouphenometry = get_1_acouphenometry()
print(data_acouphenometry)'''


'''
d_activities, count_error = list_activities_one_user()

print(d_activities,count_error)'''

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

sns.pairplot(plot_all_activities())
