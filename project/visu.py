import json
import matplotlib.pyplot as plt

from project.explore import get_1_acouphenometry

def display_1_acouphenometry():
    data_acouphenometry = get_1_acouphenometry()
    points = data_acouphenometry["data"]["points"]
    f = [point["f"] for point in points]
    q = [point["q"] for point in points]
    plt.plot(q,f)
    plt.scatter(q[-1],f[-1],c="red",s=100)
    plt.xlim(1,0)
    plt.ylim(0,1)
    plt.axis("equal")
    plt.show()

def display_trajectory(i=1,file = "data/dtrajectories.json"):
    """
    To execute this function you must have executed get_trajectories_acouphenometry once before.
    """
    with open(file) as input_file:
        trajectories = json.load(input_file)
    keys = trajectories.keys()
    key = list(keys)[i]
    points = trajectories[key]
    f = [point["f"] for point in points]
    q = [point["q"] for point in points]
    plt.plot(q,f)
    plt.scatter(q[-1],f[-1],c="red",s=100)
    plt.xlim(1,0)
    plt.ylim(0,1)
    plt.show()