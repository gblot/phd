from TimeGraph import *
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from outils import *
import rpy2.robjects as robjects
import pickle

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class MyFuncs:
    
    #Renvoie la recommandation à partir du Time Graph
    #fic1 => TimeStamps
    #fic2 => Items
    #fic3 => Users
    #t => temps courant - temps derniere visite
    #x => derniere ressource visitee
    #profondeur => profondeur max du chemin
    #nb_res => nombre de resultats max a retourner
    def recomTG(self,fic1,fic2,fic3,t,x,profondeur,nb_res):
        #convert = robjects.r('read.table')
        #data = convert(fic,sep=",")
        #Definit les colonnes du DataFrame
        d ={'1':robjects.IntVector(fic1),'2':robjects.IntVector(fic3),'3':robjects.IntVector(fic2)}
        data = robjects.DataFrame(d)

        #Creation du Time Graph
        tg = TimeGraph()
        tg.creerTimeGraph(data)
        return tg.recommandation(t,x,profondeur,nb_res)

    #Renvoie la recommandation à partir des cycles
    #fic1 => TimeStamps
    #fic2 => Items
    #fic3 => Users
    #idUser => utilisateur demandant la recommandation
    #lastItem => derniere ressource visitée
    def recomCycles(self,fic1,fic2,fic3,idUser,lastItem):
         d ={'1':robjects.IntVector(fic1),'2':robjects.IntVector(fic3),'3':robjects.IntVector(fic2)}
         data = robjects.DataFrame(d)

         #Creation du Time Graph
         tg = TimeGraph()
         tg.creerTimeGraph(data)
         return recommandationBis(idUser,data,tg.mediane,tg.item,lastItem)
        
        
    #Fonction test d'affichage
    def test(self,x):
        print "Message" + str(x)
        return 0

server.register_instance(MyFuncs())
# Run the server's main loop
print "Serveur lance"
server.serve_forever()
