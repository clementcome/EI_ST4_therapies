import json
import matplotlib.pyplot as plt

def list_activities(file="data/des.json"):
    with open(file) as input_file:
        data = json.load(input_file)
    d_activities = {}
    count_error = 0
    for key in data.keys():
        try:
            activity = data[key]["data"]["activity"]
            if activity in d_activities.keys():
                d_activities[activity] += 1
            else:
                d_activities[activity] = 1
        except KeyError:
            count_error +=1
    return d_activities, count_error

def get_1_acouphenometry(file="data/des.json"):
    with open(file) as input_file:
        data = json.load(input_file)
    for key in data.keys():
        try:
            activity = data[key]["data"]["activity"]
            if activity == "acouphenometry":
                return data[key]
        except:
            pass

def list_activities_one_user(file="data/des.json"):
    with open(file) as input_file:
        data = json.load(input_file)
    d_users = {}
    count_error = 0
    for key in data.keys():
        try:
            user = data[key]["userKey"]
            activity = data[key]["data"]["activity"]
            if user in d_users.keys():
                #d_activities=d_users[user]
                if activity in d_users[user].keys(): #activities.key dans list_activities
                    d_users[user][activity] += 1
                else:
                    d_users[user][activity] = 1
            else:
                d_users[user]={}
                #d_activities=d_users[user]
                d_users[user][activity] = 1
        except KeyError:
            count_error +=1
    return d_users, count_error

def tinnituses_features(data='data/dsu.json'):
    with open(data) as json_es:
        abon = json.load(json_es)
    tinnituse = []
    count_error = 0
    for user in abon :
        try :
            frequence = abon[user]["reducers"]["tinnituses"][0]["frequency"]
            bandwidth = abon[user]["reducers"]["tinnituses"][0]["bandwidth"]
            tinnituse.append((frequence, bandwidth,user))
        except :
            count_error += 1
    return(tinnituse,count_error)

def freq_keepTheShape(file="data/des.json",data='data/dsu.json'): # Ne renvoie rien parce que aucun de ceux  dont on  a la fréquence de l'acouphène font keeptheshape?
    list=list_activities_one_user(file)[0]
    frequence=tinnituses_features(data)
    X=[]
    Y=[]
    count_error=0
    print(len(list))
    for user in list:
        try:
            X.append([list[user]["keepTheShape"],user])
        except KeyError:
            count_error+=1
    for freq in frequence[0]:
        Y.append([freq[0],user])
    print(len(X),len(Y))
    for x in X:
        for y in Y:
            if x[1]==y[1]:
                plt.scatter((x[0],y[0]))
                print(x[0])
    print(count_error)
    plt.show()


#plot de fréquence d'utilisation (par jour) en fonction de la même chose pour une activité différente, présenté sous forme de matrice (bin avec saeborn)

#Quel sont les deux activités qui sont faites le plus de fois?
#'keepTheShape': 6409, et 'toyFactory'

#Qui sont les gens qui ont fait  les deux?


def two_activities(file="data/des.json"):
    list_activities_one_user(f)
