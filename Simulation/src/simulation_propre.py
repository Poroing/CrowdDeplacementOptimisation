import time

def ConstruireSalle (, fichierJSON):
    hahfe = fichierJson['hauteur_rang'] 

def initialiserSimulation 

class EcouteurPersonne(self):

    def __init__(self, personne, action):
        self.personne = personne
        self.action = action
        self.personne_deja_sortie = False

    def ecouter(self, temps):
        if not self.personne_deja_sortie and personne.estSortie():
            self.action(temps)

def mettreAJourPersonneSortie():
    print('Sortie')

class ConstructeurSimulation(object):

    def __init__(self, donnees_simulation):
        constructeur_salle = ConstructeurSalle(donnees_simulation)
        self.simulation = Simulation(constructeur_salle.espace, donnees_simulation['mise_a_jour_par_seconde'])

    def contruirePersonneEtEcouteur(self, nombre_personnes):
        #Pour le moment on met un ecouteur sur chaque personne
        for _ in range(nombre_personnes):
            personne = Personne(Vec2d(random.randint(60, 40 + self.espace.lieu_ferme.largeur),
                random.randint(60, 40 + self.espace.lieu_ferme.hauteur)), self.espace))
            self.simulation.ecouteurs.append(EcouteurPersonne(personne, mettreAJourPersonneSortie))
            self.simulation.espace.ajouterPersonne(personne)

class Simulation(object):
    
    def __init__(self, espace, mise_a_jour_par_seconde, action_mise_a_jour):
        self.espace = espace
        self.mise_a_jour_par_seconde = mise_a_jour_par_seconde
        self.ecouteurs = []
        self.mise_a_jour_par_seconde = action_mise_a_jour

    def mettreAJour(self):
        self.espace.avancer(1 / self.mise_a_jour_par_seconde)
        temp_mise_a_jour = time.time() - self.debut_lancement
        for ecouteur in self.ecouteurs:
            ecouteur.ecouter(temp_mise_a_jour)
        self.mise_a_jour_par_seconde(self)

    def lancer(self):
        self.debut_lancement = time.time()
        while True:
            self.mettreAJour()
