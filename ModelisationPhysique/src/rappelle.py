
class EnsembleRappelle():

    def __init__(self):
        self.ensemble_rappelles = []

    def ajouter(self, rappele):
        self.ensemble_rappelles.append(rappele)

    def __call__(self, *args, **kwargs):
        for rappele in self.ensemble_rappelles:
            rappele(*args, **kwargs)
