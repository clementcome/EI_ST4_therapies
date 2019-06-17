import json
import datetime 
import time
import matplotlib.pyplot as plt
import numpy as np


#fghjgr
computeJson=True
visu = True


    #---EXTRACTION DES DONNEES----------------------------------
    #---PERTINENTES----------------------------------
    #---POUR ANALYSE DE----------------------------------
    #---EXAMPLE----------------------------------  

if computeJson:
    
 
    # lecture des fichiers de data (format JSON)
    with open('data/des.json') as json_es:
        es = json.load(json_es)
    print("Nombre d'event dans l'event sourcing : "  + str(len(es)))
    
    with open('data/dsu.json') as json_es:
        abon = json.load(json_es) # abonnes
    print("Nombre d'abonnes dans strongUsers: "  + str(len(abon)))

    # Creation dun dictionnaire avec les donnees pertinentes pour le besoin de example
    duserdate = dict()

    for datum in es:
        userkey = es[datum]['userKey']
        date = es[datum]['date'] #date = datetime.datetime.fromtimestamp(d)
        typeevt = es[datum]['type']

        # si c'est un abonne
        if (userkey in abon):
            # si activity complete, ajout de la date dans la liste des dates user
            if (typeevt == "ACTIVITY_COMPLETE") :
                tmp = [] # liste des dates
                if (userkey in duserdate):
                    tmp = duserdate[userkey]["listDateActivityCompleted"]
                else:
                    duserdate[userkey] = dict()
                    duserdate[userkey]["listDateActivityCompleted"]=[]
                    if ("subscriptionDate" in abon[userkey]['reducers']['user']):
                        duserdate[userkey]["subscriptionDate"] = abon[userkey]['reducers']['user']['subscriptionDate']
                    else:
                        duserdate[userkey]["subscriptionDate"] = time.time() 
                tmp.append(date)
                duserdate[userkey]["listDateActivityCompleted"] = tmp
    
    # enregistrement des donnes pertinentes
    with open('data/duserdate.json', 'w') as fp:
        json.dump(duserdate, fp, indent=2)

    print("Nombre d'abonnes avec au moins une activity complete : " + str(len(duserdate)))

    #------VISUALISATION DES DONNEES-------------------------------
    #------AFIN D AVOIR UNE IDEE-------------------------------
    #------DE CE QUE LON VA POUVOIR FAIRE-------------------------------
    #------POUR REPONDRE AU PROBLEME DE------------------------------- 
    #------EXAMPLE----------------------------------        


def getNbDaysFromNow(date):
    return round(date/(24*60*60), 0)-round(time.time()/(24*60*60), 0)

if (visu):
    with open('data/duserdate.json') as json_es:
        duserdate = json.load(json_es) # abonnes
    print("Nombre de user abonne qui utilisent Diapason : "  + str(len(duserdate)))
    i=0
    lstUser = []
    for user in list(duserdate.keys())[:20]:
        lstUser.append(user)
        val = getNbDaysFromNow(duserdate[user]['subscriptionDate'])
        if (val == 0):
            print('Date non connue : ' + user + ' ' + str(val))
        plt.plot(val, i, '.g')
        lst = duserdate[user]['listDateActivityCompleted']
        lstD = []
        for d in lst:
            lstD.append(getNbDaysFromNow(d))
        plt.plot(lstD, np.ones(len(lstD))*i, '.b', alpha=.2)
        i+=1

    plt.yticks(np.arange(i), lstUser)
    plt.title("Example de visualisation de donnees")
    plt.show()


