from pymunk.vec2d import Vec2d
import pymunk

class Personne(object):

    RAYON = 21
    MASSE = 70
    MOMENT = pymunk.moment_for_circle(MASSE, 0, RAYON)
    FORCE_DEPLACEMENT = RAYON * 10**4
    VITESSE_MAXIMALE = 222

    def __init__(self, position, lieu_ferme):
        self.body = pymunk.Body(Personne.MASSE, Personne.MOMENT)
        self.shape = pymunk.Circle(self.body, Personne.RAYON)
        self.body.position = position
        
        self.lieu_ferme = lieu_ferme

    def estSortie(self):
        return self.body.position.y < self.lieu_ferme.avoirCentrePorte().y

    def ajouterDansEspace(self, espace):
        espace.add(self.body, self.shape)

    def traiterVitesse(self):
        if self.body.velocity.length > Personne.VITESSE_MAXIMALE:
            self.body.velocity *= Personne.VITESSE_MAXIMALE / self.body.velocity.length

    def update(self):
        self.traiterVitesse()
        if not self.estSortie():
            force = (self.lieu_ferme.avoirCentrePorte() - self.body.position).normalized() * Personne.FORCE_DEPLACEMENT
            self.body.apply_force_at_local_point(force, Vec2d(0, 0))
