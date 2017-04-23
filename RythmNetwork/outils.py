from datetime import datetime
import rpy2.robjects as robjects

#Convertit une date dd/mm/yyyy hh:mm en secondes
#date -> date a convertir
#dateRef -> date de reference pour le calcul de secondes
def date_to_second(date,dateRef):
    date = date.split(" ")
    jour = date[0].split("/")
    heure = date[1].split(":")

    day = int(jour[0])
    month = int(jour[1])
    year = int(jour[2])
    
    hour = int(heure[0])
    minute = int(heure[1])
    second = int(heure[2])
    date = datetime(year,month,day,hour,minute,second)
    
    dateRef = dateRef.split(" ")
    jour = dateRef[0].split("/")
    heure = dateRef[1].split(":")

    day = int(jour[0])
    month = int(jour[1])
    year = int(jour[2])
    
    hour = int(heure[0])
    minute = int(heure[1])
    second = int(heure[2])

    dateRef = datetime(year,month,day,hour,minute,second)
    nbSec = (date-dateRef).total_seconds()
    return int(nbSec)

#Sauvegarde une variable dans un fichier RData
#var -> variable a sauvegarder
#nameVar -> nom de la variable dans l'environnement RPy
#nameFile -> nom du fichier
def save_var(var,nameVar,nameFile):
    robjects.r.assign(nameVar,var)
    robjects.r("save("+nameVar+", file = '"+nameFile+"')")

#Retourne une variable a partir d'un fichier RData
#nameVar -> nom de la variable dans l'environnement RPy
#nameFile -> nom du fichier
def load_var(nameVar,nameFile):
    robjects.r("load('"+nameFile+"')")
    return robjects.r[nameVar]

#Determine les cycles d'un utilisateur
#data -> DataFrame contenant les logs
#idUder -> utilisateur dont on cherche les cycles
#maxTime -> temps maximum entre deux ressources dans un cycle
#items -> ressources
#Retourne les cycles, les poids de ces cycles,
#un vecteur contenant le nombre de visites de chaque ressource et le temps de la derniere ressource de chaque cycle
def trouveCyclesUser(data,idUser,maxTime,items):
    cycles = list()
    poidsCycles = list()
    matUI = [0] * len(items)
    time = list()
    lastTime = -1 #Temps de la derniere ressource
    lastVisit = -1#Derniere ressource
    nb = -1
    taille = robjects.r.length(data[0])[0]

    #Parcours des logs
    for i in range(taille-1,-1,-1):

        if data[2][i] == idUser:
            #Si la derniere ressource visitee est differente de la ressource courante
            if lastVisit != data[1][i]:
                id = items.index(data[1][i])
                matUI[id] += 1

                #Si le temps entre les deux ressources est plus petite que maxTime, on continue le cycle
                if lastTime != -1 and data[0][i] - lastTime < maxTime:
                    cycles[nb] += ":" + str(data[1][i])
                    poidsCycles[nb] += data[0][i] - lastTime
                #Sinon on commence un nouveau cycle
                else:
                    if lastTime != -1:
                        time.append(lastTime)
                    #Si le dernier cycle est compose que d'une ressource, on l'enleve
                    if nb != -1 and poidsCycles[nb] == 0:
                        poidsCycles.pop()
                        cycles.pop()
                        nb -= 1
                
                    nb += 1
                    cycles.append(str(data[1][i]))
                    poidsCycles.append(0)
                lastTime = data[0][i]
                lastVisit = data[1][i]
    #Si le dernier cycle est compose que d'une ressource, on l'enleve
    if nb != -1 and poidsCycles[nb] == 0:
        poidsCycles.pop()
        cycles.pop()
        nb -= 1
    return(cycles,poidsCycles,matUI,time)

#Determine les cycles de tous les utilisateurs
#data -> DataFrame contenant les logs
#maxTime -> temps maximum entre deux ressources dans un cycle
#items -> ressources
#Retourne les cycles, les poids de ces cycles,
#un vecteur contenant le nombre de visites de chaque ressource et le temps de la derniere ressource de chaque cycle
def trouveCycles(data,maxTime,items):
    unique = robjects.r("unique")
    tri = robjects.r("sort")
    users = list(tri(unique(data[2])))
    cycles = list()
    poidsCycles = list()
    matUI = [0] * len(items) * len(users)
    time = list()
    cpt = 0

    for i in users:
        cycleTmp,poidsTmp,matUITmp,timeTmp = trouveCyclesUser(data,i,maxTime,items)
        cycles.append(cycleTmp)
        poidsCycles.append(poidsTmp)
        time.append(timeTmp)

        for j in range(len(items)):
            matUI[cpt * len(items) + j] = matUITmp[j]
        cpt += 1
            
    
    return(cycles,poidsCycles,matUI,time)

#Renvoie les cycles et les utilisateurs possedant ces cycles
def groupeCycles(cycles,users):
    groupes = list()
    userGroupe = list()
    for i in range(len(cycles)):
        for j in range(len(cycles[i])):
            if cycles[i][j] not in groupes:
                groupes.append(cycles[i][j])
                userGroupe.append(str(users[i]))
            else:
                id = groupes.index(cycles[i][j])
                userGroupe[id] += ',' + str(users[i])
    return (groupes,userGroupe)

#Compte le nombre de cycles communs entre deux utilisateurs
def cyclesCommuns(cycles,user1,user2):
    cpt = 0
    for c in cycles[user1]:
        if c in cycles[user2]:
            cpt += 1
    return cpt

#Retourne un vecteur contenant le nombre de cycles en communs (mat[i *nbUser + j] => nombre de cycles en communs entre i et j)
def allCyclesCommuns(cycles):
    nbUsers = len(cycles)
    mat = [0] * nbUsers * nbUsers
    for i in range(0,nbUsers):
        for j in range(i+1,nbUsers):
            tmp = cyclesCommuns(cycles,i,j)
            mat[i*nbUsers+j] = tmp
            mat[j*nbUsers+i] = tmp
    return mat
"""
def compareCycles(c1,c2,time1,time2):
    for i in len(c1)
"""   


#Retourne le numero de l'utilisateur ayant le plus de cycles en communs avec idUser
def bestCycles(mat,idUser,nbUsers):
    x = max(mat[idUser*nbUsers:(idUser+1)*nbUsers-1])
    print x
    return mat[idUser*nbUsers:(idUser+1)*nbUsers-1].index(x)

#Retourne la similarite cosinus entre x et y                
def cosSim(x,y):
    robjects.r.assign('x',x)
    robjects.r.assign('y',y)
    return robjects.r('x %*% y / sqrt(x%*%x * y%*%y)')[0]

#Retourne la ressource visite par un utilisateur juste apres time et le temps de la visite
def getNext(data,time,user,item):
    match = robjects.r("match")
    id = match(time,data[0])[0] - 1
    retourI = -1
    retourT = -1
    #Trouver item
    while id >= 0 and data[2][id] != user and data[1][id] != item:
        id -= 1
    
    id -= 1
    if id >= 0:
        #Trouver la ressource suivante d'item
        while id >= 0 and data[2][id] != user:
            id -= 1
        if id >= 0:
            retourI = data[1][id]
            retourT = data[0][id]
        else:
            a = 1
            #print "Pas trouve suivant"
    else:
        a = 2
        #print "Pas trouve dernier visite"
    
    return retourI,retourT


def recommandationBis(idUser,data,seuil,items,lastItem,cycles = -1,matUI = -1, time = -1, mat = -1):
    unique = robjects.r("unique")
    tri = robjects.r("sort")
    users = list(tri(unique(data[2])))
    #Si les cycles ne sont pas fournis, ils sont calcules
    if cycles == -1:
        cycles,poidsCycles,matUI,time = trouveCycles(data,seuil,items)
        mat = allCyclesCommuns(cycles)

    #Recupere le numero de la case du user
    numUser = users.index(idUser)
    v = mat[numUser*len(cycles):(numUser+1)*len(cycles)]

    x = matUI[numUser * len(items) : (numUser+1)*len(items)]
    saveV = list(v)

    #Recupere le nombre de cycles en commun maximum
    maxi = max(v)
    nextI = -1

    while maxi > 0 and nextI == -1:
        for i in range(len(v)):
            #Si le nombre de cycle commun est le max, on calcule la similarite
            if v[i] == maxi:
                y = matUI[i * len(items) : (i+1)*len(items)]
                v[i] *= cosSim(robjects.IntVector(x),robjects.IntVector(y))
    
            #Sinon on l'ecarte
            else:
                v[i] = -1


        maxi = max(v)
        

        #Recupere l'utilisateur le plus similaire
        numUser2 = v.index(max(v))
        idUser2 = users[numUser2]
        i = len(cycles[numUser]) - 1
        #Recupere le dernier cycle commun
        while cycles[numUser][i] not in cycles[numUser2]:
            i -= 1
           
        idCycle = cycles[numUser2].index(cycles[numUser][i])
        temps = time[numUser2][idCycle]
        c = cycles[numUser2][idCycle].split(",")
        nextI,nextT = getNext(data,temps,idUser2,c[len(c)-1])
        #Recupere le temps de la visite de lastItem juste apres le dernier cycle commun
        while nextI != -1 and nextI != lastItem:
            nextI,nextT = getNext(data,nextT,idUser2,nextI)

        #Si la ressource a ete trouve, recupere celle visitee apres
        if nextI != -1:
            while nextI == lastItem:
                nextI,nextT = getNext(data,nextT,idUser2,nextI)
        saveV[numUser2] = -1
        v = list(saveV)
        maxi = max(v)

    return nextI
