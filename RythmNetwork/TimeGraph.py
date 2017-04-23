import rpy2.robjects as robjects
import rpy2.rinterface as rinterface
import re
from outils import *
from _gexf import Gexf

class TimeGraph:
        
	nbTG = 0

	def __init__ (self):
                self.id = TimeGraph.nbTG
                self.user = -1
                self.item = list() #numero de tous les items
                #self.matrice
                #self.mediane
                TimeGraph.nbTG += 1

        def __getitem__(self):
                return self.item

        #data -> DataFrame contenant les logs
        #seuil_temps -> seuil en secondes, si le temps entre deux ressources est superieur, il n'est pas pris en compte
        #seuil_visites -> seuil minimum de visites pour qu'une arete soit gardee dans le Time Graph
        #nbsave -> frequence de sauvegarde en nombre d'aretes
	def creerTimeGraph(self, data, seuil_temps = 9999999999, seuil_visites = 0, nb_save = -1):
                saveData = open("save.txt",'w')
                cptSave = 0
                unique = robjects.r("unique")
                taille = robjects.r.length(data[0])
                last = list() #indice de data du dernier sommet visite
                users = list()
                poidsTmp = list()
                edge = list()
                #Premier parcours: recuperer les users et les items 
                """for i in range(taille[0]):
                        if data[1][i] not in self.item:
                                self.item.append(data[1][i])
                        if data[2][i] not in users:
                                users.append(data[2][i])
                """
                self.item = list(unique(data[1]))
                users = list(unique(data[2]))
                print "Taille User: "+str(len(users))
                last =[-1] * len(users)

                nbItem = len(self.item)

                #Deuxieme parcours: effectuer les connexions
                for i in range(taille[0] -1,-1,-1):

                        id = users.index(data[2][i])

                        #Si l'utilisateur a deja visite une ressource
                        if last[id] != -1:
                                #Si la ressource actuelle et la derniere visitee sont differentes
                                if data[1][last[id]] != data[1][i]:
                                        poids = data[0][i] - data[0][last[id]]

                                        if poids < seuil_temps:
                                                
                                                arete = str(data[1][last[id]]) + "-" + str(data[1][i])

                                                if arete not in edge:
                                                        poidsTmp.append(str(poids))
                                                        edge.append(arete)
                                                        cptSave += 1

                                                        #Sauvegarde dans le fichier
                                                        if cptSave == nb_save :
                                                                cptSave = 0
                                                                buff = str(poidsTmp) + "*" + str(edge) + "/"
                                                                saveData.write(buff)
                                                                poidsTmp = list()
                                                                edge = list()
                                                else:
                                                        poidsTmp[edge.index(arete)] += ":" + str(poids)
                        last[id] = i

                if len(poidsTmp) != 0 :
                        buff = str(poidsTmp) + "*" + str(edge)
                        
                saveData.write(buff)
                poidsTmp = list()
                edge = list()
                saveData.close()

                #Recuperation des aretes dans le fichier de sauvegarde
                saveData = open("save.txt",'r')
                lecture = saveData.read()
                
                #Separation des aretes
                lecture = lecture.split("/")
                if(lecture[len(lecture)-1] == ''):
                        lecture.remove('')
                
                #Separation poids/aretes
                separe = lecture[0].split("*")

                poidsTmp = separe[0]
                edge = separe[1]

                #Enlever les crochets
                poidsTmp = poidsTmp[1:len(poidsTmp) - 1]
                edge = edge[1:len(edge) - 1]

                #Recuperer les chaines sous forme de listes
                poidsTmp = poidsTmp.split(',')
                edge = edge.split(',')
               

                for i in range(1,len(lecture)):
                        separe = lecture[i].split("*")
                        separe[0] = separe[0].split(",") #poids des aretes
                        separe[1] = separe[1].split(",") #aretes

                        #Enleve les caracteres non voulus
                        separe[1][0] = separe[1][0].replace("[","")
                        separe[1][len(separe[1])-1] = separe[1][len(separe[0])-1].replace("]","")
                        separe[0][0] = separe[0][0].replace("[","")
                        separe[0][len(separe[0])-1] = separe[0][len(separe[0])-1].replace("]","")
                        
                        #On verifie si les aretes trouvees existent deja
                        for j in range(0,len(separe[1])):
                                if separe[1][j] not in edge:
                                        edge.append(separe[1][j])
                                        poidsTmp.append(separe[0][j])
                                else:
                                        id = edge.index(separe[1][j])
                                        poidsTmp[id] = poidsTmp[id] + ":"+ separe[0][j]
                saveData.close()


                self.item.sort()

                self.matrice = [-1] * nbItem * nbItem

                
                chercheSeuil = list() #Permet de recuperer la moyenne et la medianne de tous les temps entre deux visites

                for i in range(len(poidsTmp)):

                        #Recupere le poids et les sommets des aretes
                        poidsArete = poidsTmp[i].split(':')
                        arete = edge[i].split('-')

                        #enlever les ' des listes
                        for i in range(0,len(poidsArete)):
                                poidsArete[i] = poidsArete[i].replace("'",'')
                        
                        for i in range(0,len(arete)):
                                arete[i] = arete[i].replace("'",'')
                        
                        #Moyenne des poids de l'arete
                        if(len(poidsArete) >= seuil_visites):
                                poids = robjects.IntVector(poidsArete)
                                moy = (robjects.r('mean')(poids))[0]
                                x = self.item.index(int(arete[0]))
                                y = self.item.index(int(arete[1]))
                                self.matrice[x * nbItem + y] = moy
                                for i in range(0,len(poidsArete)):
                                        chercheSeuil.append(int(poidsArete[i]))

                                #savePoids[x*nbItem+y] = poidsArete[0]
                                #for i in range(1,len(poidsArete)):
                                #        savePoids[x*nbItem+y] += ":"+str(poidsArete[i])
                vect = robjects.IntVector(chercheSeuil)
                self.mediane = (robjects.r('median')(vect))[0]
                print "Moyenne: " + str((robjects.r('mean')(vect))[0])
                print "Mediane: " + str((robjects.r('median')(vect))[0])
                #save_var(robjects.StrVector(savePoids),'poids','poids.RData')


       

        #Permet d'afficher le Time Graph
        def afficher(self):
                nbItem = len(self.item)
                print ''
                print 'Graphe numero ' + str(self.id)
                print "Items:"
                print self.item
                print ""

                for i in range(nbItem):
                        print "\t" + str(self.item[i]),
                print ''
                
                for i in range(nbItem):
                        print str(self.item[i]) + "\t",
                        for j in range(nbItem):
                                print str(self.matrice[i*nbItem+j]) + "\t",
                        print ""

                print ''
        
        #Recupere la ligne de la matrice d'adjacence de x
        def getArete(self,x):
                nbItem = len(self.item)
                id = self.item.index(x)
                return self.matrice[id*nbItem:(id+1)*nbItem]

        
        #Fonction recursive qui trouve tous les chemins allant jusque fin ayant un poids inferieur ou egal a t
        #t-> temps courant - temps de la ressource visitee
        #courant -> ressource courante
        #fin -> ressource que l'on cherche a atteindre
        #poids -> poids du chemin actuel
        #chemin -> chemin actuel
        #cpt -> nombre maximum de sommets restants a visiter
        def parcoursRecom(self,t,courant,fin,poids,chemin,cpt):
                listeSuivant = self.getArete(courant)
                poidsTmp = poids

                for i in range(len(listeSuivant)):
                        poids = poidsTmp
                        #Si i est un voisin de courant
                        if listeSuivant[i] != -1:
                                poids = poidsTmp + listeSuivant[i]
                                #Si le chemin n'a pas un poids trop eleve
                                if t - poids >= 0:
                                        if int(self.item[i]) == int(fin):
                                                listePoids.append(t - poids)
                                                listeChemins.append(chemin +"," + str(self.item[i]))
                                        else:
                                                if cpt > 1:
                                                        cheminNext = chemin + ',' + str(self.item[i])
                                                        self.parcoursRecom(t,self.item[i],fin,poids,cheminNext,cpt-1)
        
        #Retourne tous les chemins recommandes
        #Retourne les chemins recommandes
        #t -> temps courant - temps de la ressource visitee
        #x -> ressource courante
        #profondeur -> pronfondeur maximale du chemin
        #nb_res -> nombre de resultats voulus
        def recommandation(self,t,x,profondeur,nb_res):
                global listePoids
                global listeChemins
                listePoids = list()
                listeChemins = list()

                #Pour tous les items
                for y in self.item:
                        if y != x:
                                self.parcoursRecom(t,x,y,0,str(x),profondeur)
                retour = list()
                cpt = 0
                #Recupere les nb_res plus petits resultats
                while cpt < nb_res and len(listePoids) > 0:
                        retour.append(min(listePoids))
                        id = listePoids.index(retour[cpt*2])
                        retour.append(listeChemins[id])
                        del listeChemins[id]
                        del listePoids[id]
                        cpt += 1
                return retour

        #Sauvegarde le Time Graph dans un fichier RData
        def saveTG(self,nameFile):
                robjects.r.assign("item",robjects.IntVector(self.item))
                robjects.r.assign("id",self.id)
                robjects.r.assign("matrice",robjects.FloatVector(self.matrice))
                robjects.r("save(item,id,matrice,file='"+nameFile+"')")

        #Recupere le Time Graph dans un fichier RData
        def loadTG(self,nameFile):
                robjects.r("load('"+nameFile+"')")
                self.id = robjects.r['id'][0]
                self.item = list(robjects.r['item'])
                self.matrice = list(robjects.r['matrice'])

        #Sauvegarde le Time Graph dans un fichier au format Gexf
        def toGexf(self,nameFile):
                gexf = Gexf("Dylan Gerard","Time Graph Description")
                graph = gexf.addGraph("directed","static",str(self.id))
                for i in range(len(self.item)):
                        graph.addNode(str(self.item[i]),str(self.item[i]))
                for i in range(len(self.item)):
                        for j in range(len(self.item)):
                                if self.matrice[i*len(self.item)+j] != -1:
                                        buff = str(self.item[i]) + ":" + str(self.item[j])
                                        graph.addEdge(buff,str(self.item[i]),str(self.item[j]),weight = self.matrice[i*len(self.item)+j])
                output_file = open(nameFile,'w')
                gexf.write(output_file)
        
        #Recupere le Time Graph dans un fichier auformat Gexf
        def fromGexf(self,nameFile):
                self.item = list()
                f = open(nameFile,'r')
                gexf = Gexf.importXML(f)
                graph=gexf.graphs[0]
                self.id = int(graph.label)
                # display nodes list 
                for node_id,node in graph.nodes.iteritems() : 
                        self.item.append(int(node.label))
                self.item.sort()
                nbItems = len(self.item)
                self.matrice = [-1] * nbItems * nbItems
                # display edges list 
                for edgeid,edge in graph.edges.iteritems() :
                        x = self.item.index(int(edge.source))
                        y = self.item.index(int(edge.target))
                        self.matrice[x * nbItems + y] = edge.weight

                
        






		
