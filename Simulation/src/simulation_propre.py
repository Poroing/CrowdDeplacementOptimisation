def ConstruireSalle (, fichierJSON):
    hahfe = fichierJson['hauteur_rang'] 

def initialiserSimulation 

class Simulation(object):
    
    def __init__(self, type_de_salle, temps_execution, largeur_ecran = 1000, hauteur_ecran = 1000):
        
        self.bibliotheque = bibliotheque[type_de_salle]
        self.largeur_ecran = largeur_ecran
        self.hauteur_ecran = hauteur_ecran
        self.temps_execution = temps_execution
    
    def ajouterObstacles(self,lieu_ferme, bibliotheque):
        posGauche = int(bibliotheque['position_premier_obstacle_gauche'])
        posDroite = int(bibliotheque['position_premier_obstacle_droit'])
    
        while posGauche + 50 <= bibliotheque['hauteur_salle'] :
            lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(int( bibliotheque['hauteur_obstacle']),int(bibliotheque['largeur_obstacle']),(int(bibliotheque['distance_mur_rang']),posGauche)))
            posGauche += int(bibliotheque['distance_entre_deux_obstacles'])
        
        while posDroit + 50 <= bibliotheque['hauteur_salle'] :
            lieu_ferme.ensemble_obstacle.append(ObstacleRectangulaire(int( bibliotheque['hauteur_obstacle']),int(bibliotheque['largeur_obstacle']),(50 +int( bibliotheque['largeur_salle']) + int(bibliotheque['distance_mur_rang']),posDroit)))
            posDroit += int(bibliotheque['distance_entre_deux_obstacles'])
        
        
    def ajouterPersonnes(self, bibliotheque
    
        for _ in range ( int( bibliotheque['nombre_de_personnes'] ) ) :
            lieu_ferme.ensemble_personnes.append(
                Personne(Vec2d(random.randint(60, 40+ lieu_ferme.largeur),
                    random.randint(60, 40 + lieu_ferme.hauteur)), lieu_ferme))

        lieu_ferme.ajouterDansEspace(espace)
    
    def construireEspace(self, bibliotheque):
        IMAGE_PAR_SECONDE = 60
        horloge = pygame.time.Clock()

        ecran = pygame.display.set_mode((hauteur_ecran, largeur_ecran))
        option_dessin = pymunk.pygame_util.DrawOptions(ecran)

        espace = pymunk.Space()
        lieu_ferme = LieuFerme(float(bibliotheque['largeur_salle']),float(bibliotheque['hauteur_salle']),Vec2d(50, 50), float(bibliotheque['position_porte']), float(bibliotheque['largeur_porte'] )
        ajouterObstacles(lieu_ferme, bibliotheque)
        