import time
import base

class Simulation(object):
    '''S'occupe d'ajouter les écouteurs aux personnes de l'espace
    et de mettres à jour tous les éléments nécessaire à la
    simulation lorsqu'il lui est demandé

    creer_ecouteur: une fonction prenant une personne en entree et
        renvoyant un ecouteur associé à cette personne

    '''

    AUCUN = 0x0
    ARRET = 0x1
    TOGGLE_PAUSE = 0x2
    
    def __init__(self, espace, nombre_mise_a_jour_par_seconde, creer_ecouteur):
        self.espace = espace
        self.mise_a_jour_par_seconde = nombre_mise_a_jour_par_seconde
        self.ecouteurs = []
        self.sources = []
        self.action_mise_a_jour = lambda simulation: None
        self.en_marche = False

        self.creer_ecouteur = creer_ecouteur

        self.espace.rappelle_personne_ajoute = base.EnsembleRappelle()
        self.espace.rappelle_personne_ajoute.ajouter(self.ajouterEcouteurPourPersonne)

    @property
    def rappelle_personne_ajoute(self):
        return self.espace.rappelle_personne_ajoute

    @property
    def ensemble_personnes(self):
        return self.espace.ensemble_personnes

    def mettreAJour(self):
        self.temps_depuis_lancement += 1 / self.mise_a_jour_par_seconde
        self.espace.avancer(1 / self.mise_a_jour_par_seconde)
        for ecouteur in self.ecouteurs:
            ecouteur.ecouter(self.temps_depuis_lancement)
        self.mettreAJourSource()

    def ajouterEcouteurPourPersonne(self, personne):
        self.ecouteurs.append(self.creer_ecouteur(personne))

    def gererActionExterieur(self):
        commande = self.action_mise_a_jour(self)
        self.executerCommande(commande)

    def mettreAJourSource(self):
        for source in self.sources:
            source.mettreAJour(self.temps_depuis_lancement)

    def executerCommande(self, commande):
        if commande & Simulation.ARRET:
            self.en_marche = False
        if commande & Simulation.TOGGLE_PAUSE:
            self.en_pause = not self.en_pause

    def lancer(self):
        self.debut_lancement = time.time()
        self.temps_depuis_lancement = 0
        self.en_marche = True
        self.en_pause = False
        while self.en_marche:
            self.gererActionExterieur()
            if self.en_pause:
                continue
            self.mettreAJour()

