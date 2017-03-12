## Objet Batiment

class Batiment (object):
    """ Un batiment regroupe les différentes composantes connexes des graphes de salles
        Un batiment contiens : -un nom representant le batiment 
                               -une liste des sorties (qui peuvent etre connexes)"""
    
    
    def __init__( self, nom, sorties):
        """ Construit un batiment avec les parametres donnés :
            batiment( self, nom, sorties)
            nom = String
            sorties = list(Salles)                                                                                          """
        self.nom = nom              #int
        self.sorties = sorties      #list(Salles)
    
    
    def sortiesUniques( self):
        """ sortiesUniques trouve les differentes sorties uniques non Connexes.
            On a ainsi exactement une sortie par composante connexe"""         
        groupesConnexes = []        
        # Soit la relation d'equivalence A~B de l'ensemble des sorties tel que :
        # A~B <=> Sortie A est connexe à Sortie B
        # On trouve les classes d'equivalences et on prend un representant pour chaque classe
        for k in self.sorties :
            if not presenceElementListe( k, groupesConnexes):                
                groupesConnexes.append(k.sortieConnexe())
        return [ groupe[0] for groupe in groupesConnexes]


    def salles( self):
        """renvoie toutes les salles du batiment"""
        #On applique le parcours de fonction avec l'identité pour avoir la liste des salles
        for k in self.sorties:
            salles = mapGraphe(k,(lambda x:x))
            return salles
        

    def tourSuivant( self):
        """ tourSuivant fais passer le batiment au tour suivant en appliquant parcoursGrapheFonction sur toutes les racines non Connexes"""
        
        
        def parcoursGrapheFonction(salleActuelle):
            """ parcoursGrapheFonction va appliquer la methode etatSuivant à toutes les salles connexes de la salle donnée en parametre"""
            
            #si la salle donée est une sortie, on fais passer cette sortie à un état suivant
            if salleActuelle.estSortie :
                precedents = [k[0] for k in salleActuelle.sallesAdjacentes if k[1]<0]
                salleActuelle.aEteVisite = True
                salleActuelle.etatSuivant()
                for sallePrecedente in precedents :
                    if not sallePrecedente.aEteVisite :
                        parcoursGrapheFonction( sallePrecedente)
                salleActuelle.aEteVisite = False
            #si la salle donnée n'est pas une sortie on vérifie que toutes les salles suivantes ont été actualisées
            else :
                precedents = [k[0] for k in salleActuelle.sallesAdjacentes if k[1]<0]
                suivants = [k[0] for k in salleActuelle.sallesAdjacentes if k[1]>0]
    
                for salleSuivante in suivants :
                    if not salleSuivante.aEteVisite :
                        parcoursGrapheFonction( salleSuivante)
                        
                salleActuelle.aEteVisite = True
                salleActuelle.etatSuivant()
            
                for sallePrecedente in precedents :
                    if not sallePrecedente.aEteVisite :
                        parcoursGrapheFonction( sallePrecedente)  
                        
                salleActuelle.aEteVisite = False


        sortiesNonConnexes = self.sortiesUniques()
        for sortie in sortiesNonConnexes :
            parcoursGrapheFonction(sortie)

    def efficacite( self):
        nombreTotal = 446
        # for sortie in self.sorties :
        #     for k in parcoursGraphe(sortie,lambda salle:salle.nombrePersonnes):
        #         nombreTotal+=k
        # print(nombreTotal)
        sortis = 0
        tour = 0
        while sortis<nombreTotal:
            tour+=1
            self.tourSuivant()
            sortis=0
            for k in self.sorties:
                sortis+=k.nombrePersonnes
        return tour
            
                
                
                    
        
        
        
        
        
        
        