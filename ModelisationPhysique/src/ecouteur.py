
class EcouteurPersonne(object):

    dernier_identifiant_ecouteur = -1

    def __init__(self, personne, action):
        self.initialiserIdentifiant()

        self.personne = personne
        self.action = action
        self.personne_deja_sortie = False

        self.mettreAJourPointSuiviePersonne(self.personne.test_direction)
        self.personne.test_direction.rappelle_update = self.mettreAJourPointSuiviePersonne

    def initialiserIdentifiant(self):
        self.identifiant = EcouteurPersonne.dernier_identifiant_ecouteur + 1
        EcouteurPersonne.dernier_identifiant_ecouteur += 1

    def mettreAJourPointSuiviePersonne(self, test_point_suivre):
        self.point_suivie_personne = test_point_suivre.point_a_suivre

    def ecouter(self, temps):
        if not self.personne_deja_sortie and self.personne.estSortie():
            self.personne_deja_sortie = True
            self.executerAction(temps)

    def executerAction(self, temps):
        #Seul moyen d'appeler la fonction self.action sans passer self comme
        #premier argument
        _action = self.action
        _action(temps)
