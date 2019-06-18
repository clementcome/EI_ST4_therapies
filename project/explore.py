import json
import matplotlib.pyplot as plt
import pandas

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

def list_activities_one_user_corr(file="data/des.json"): #Version corrigée qui ne prend pas en compte "guidedTour"
    with open(file) as input_file:
        data = json.load(input_file)
    d_users = {}
    count_error = 0
    for key in data.keys():
        try:
            user = data[key]["userKey"]
            activity = data[key]["data"]["activity"]
            type=data[key]["data"]["referrer"]["type"]
            if type != "guidedTour":
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
#Dans le comptage des activités, certaines étaient obligatoires quand il y avait une visite guidée donc il ne faut pas
# compter les [data][referrer][type]= "guidedTour"


def plot_two_activities(file="data/des.json"): #liste des utilisateurs qui ont fait les deux activités 'keepTheShape': 6409, et 'toyFactory'
    list=list_activities_one_user_corr(file)[0]
    users=[]#liste des utilisateurs qui ont fait les deux activités 'keepTheShape': 6409, et 'toyFactory'
    for user in list.keys():
        if 'keepTheShape'in list[user].keys() and 'toyFactory' in list[user].keys():
            users.append(user)
    X=[]
    Y=[]
    for user in users:
        X.append(list[user]["keepTheShape"])
        Y.append(list[user]["toyFactory"])
    return X,Y

#Pour faire la matrix plot. Il faut un data frame : en colonne les activités (clef du dict), en ligne les observations (un utilisateur, liste de valeurs)

def plot_all_activities(file="data/des.json"): #liste des utilisateurs qui ont fait les deux activités 'keepTheShape': 6409, et 'toyFactory'
    list_act=[activity for activity in list_activities()[0].keys()]
    list_activities_one_user=list_activities_one_user_corr()[0]

    users=[x for x in list_activities_one_user.keys()]#liste des utilisateurs qui ont fait toutes les activité. En fait non #Aucun utilisateur n'a fait toutes les activités

    plot={}

    for activity in list_act:
        nb=[0]*len(users)
        print (users)
        count_error=0
        for k,user in enumerate(users):
            try:
                nb[k]=list_activities_one_user[user][activity]
            except KeyError:
                count_error +=1
            #print(list_activities_one_user[user][activity])
        print(nb)
        plot[activity]=nb
    print("count_error ",count_error)
    print(pandas.DataFrame(plot))
    return pandas.DataFrame(plot)

