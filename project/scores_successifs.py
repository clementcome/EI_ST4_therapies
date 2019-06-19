import json

"""
Donne un dictionnaire d'activités. Pour chaque activité, un utilisateur. Pour chaque utilisateur, le score et la date."""

#scores successifs pour une activité [ des[data][gameScore] + des[userKey] where des[type] = “ACTIVITY_COMPLETE” ]
def score(file="data/data_activity.json",ouput_path="data/scores_successifs.json"):
    activities={}
    with open(file) as input_file:
        data = json.load(input_file)["es"]
    #print(data)
    for des in data.keys():
        #print(des)
        if data[des]["type"]=='ACTIVITY_COMPLETE':
            #print(data[des]["data"])
            try:
                if data[des]["data"]["activity"] not in activities.keys():
                    activities[data[des]["data"]["activity"]]={}
                    #print(activities)
                    #input("Press Enter to continue...")
                if data[des]["userKey"] not in activities[data[des]["data"]["activity"]].keys():
                    print('kjvbfrljn')
                    print([data[des]["data"]["score"],(data[des]["date"])])
                    # print(data[des])
                    # print(data[des]["userKey"])
                    activities[data[des]["data"]["activity"]][data[des]["userKey"]]=[]  #Liste qui contiendra les scores et leur date
                    activities[data[des]["data"]["activity"]][data[des]["userKey"]].append([data[des]["data"]["score"],(data[des]["date"])])

                else:
                    activities[data[des]["data"]["activity"]][data[des]["userKey"]].append([data[des]["data"]["score"],(data[des]["date"])])
                #print([data[des]["data"]["score"],(data[des]["date"])])

            except:
                    pass
    with open(ouput_path,'w') as output_file:
        json.dump(activities,output_file)
    return activities

#print (score())

#On peut tracer, pour chaque utilisateur le score en fonction du temps pour les activités, le score moyen en fonction du temps de tous les utilisateurs

