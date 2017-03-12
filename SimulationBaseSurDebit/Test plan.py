## création du plan de l'etage TIPE

#On crée toutes les salles de classe (26 à 36)

salle26 = Salle(40,80,"Salle 26")
salle27 = Salle(40,80,"Salle 27")
salle28 = Salle(40,80,"Salle 28")
salle29 = Salle(40,80,"Salle 29")
salle30 = Salle(40,80,"Salle 30")
salle31 = Salle(40,80,"Salle 31")
salle32 = Salle(40,80,"Salle 32")
salle33 = Salle(40,80,"Salle 33")
salle34 = Salle(40,80,"Salle 34")
salle35 = Salle(40,80,"Salle 35")
salle36 = Salle(40,80,"Salle 36")

# on crée le secrétariat, le bureau du proviseur adjoint et autres 

secretariat = Salle(4,15,"Secretariat")
bureauProviseur = Salle(2,6,"Bureau du proviseur")


# on crée les couloirs entre les salles

couloirAdministratif = Salle(0,35,"Couloir secretariat")
couloirsalle36 = Salle(0,20,"Couloir salle 36")
couloirSalle33 = Salle(0,35,"couloir salle 33")
couloirSalle32 = Salle(0,32,"couloir salle 32")
couloirSalle30 = Salle(0,35,"couloir salle 30")
couloirSalle28 = Salle(0,35,"couloir salle 28")
couloirSalle26 = Salle(0,35,"couloir salle 26")
couloirSalle34 = Salle(0,35,"couloir salle 34")
couloirSalle35 = Salle(0,35,"couloir salle 35")

# on crée les sorties

sortieSalle36 = Salle(0,Salle.INFINI,"Sortie salle 36",True)
sortieSalle35 = Salle(0,Salle.INFINI,"Sortie salle 35",True)
sortieEscalier = Salle(0,Salle.INFINI,"Sortie escaliers",True)

# on ajoute les liens entre salles


couloirAdministratif.ajouterAdjacent(secretariat,Salle.CHEMIN_RENTRANT_FIXE)
couloirAdministratif.ajouterAdjacent(bureauProviseur,Salle.CHEMIN_RENTRANT_FIXE)

couloirsalle36.ajouterAdjacent(couloirAdministratif,Salle.CHEMIN_RENTRANT_MUTABLE)
couloirsalle36.ajouterAdjacent(salle36,Salle.CHEMIN_RENTRANT_FIXE)
couloirsalle36.ajouterAdjacent(couloirSalle33,Salle.CHEMIN_RENTRANT_MUTABLE)
couloirsalle36.ajouterAdjacent(sortieSalle36,Salle.CHEMIN_SORTANT_MUTABLE)
couloirSalle33.ajouterAdjacent(salle33,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle33.ajouterAdjacent(couloirSalle32,Salle.CHEMIN_RENTRANT_MUTABLE)
couloirSalle33.ajouterAdjacent(couloirSalle34,Salle.CHEMIN_RENTRANT_MUTABLE)

couloirSalle34.ajouterAdjacent(couloirSalle35,Salle.CHEMIN_SORTANT_MUTABLE)
couloirSalle34.ajouterAdjacent(salle34,Salle.CHEMIN_RENTRANT_FIXE)

couloirSalle35.ajouterAdjacent(sortieSalle35,Salle.CHEMIN_SORTANT_MUTABLE)
couloirSalle35.ajouterAdjacent(salle35,Salle.CHEMIN_RENTRANT_MUTABLE)

couloirSalle32.ajouterAdjacent(couloirSalle30,Salle.CHEMIN_RENTRANT_MUTABLE)
couloirSalle32.ajouterAdjacent(salle32,Salle.CHEMIN_RENTRANT_FIXE)

couloirSalle30.ajouterAdjacent(salle30,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle30.ajouterAdjacent(salle31,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle30.ajouterAdjacent(salle29,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle30.ajouterAdjacent(couloirSalle28,Salle.CHEMIN_BLOQUE)

couloirSalle28.ajouterAdjacent(salle28,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle28.ajouterAdjacent(salle27,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle28.ajouterAdjacent(couloirSalle26,Salle.CHEMIN_SORTANT_MUTABLE)

couloirSalle26.ajouterAdjacent(salle26,Salle.CHEMIN_RENTRANT_FIXE)
couloirSalle26.ajouterAdjacent(sortieEscalier,Salle.CHEMIN_SORTANT_MUTABLE)


BatimentPrepa = Batiment("Batiment Prepa",[sortieSalle36,sortieSalle35,sortieEscalier])


## batiment Internat













