## Couplage

#Types de salles 

SALLE_VIDE = 'sale_vide'
SALLE_CLASSE = 'salle_de_classe'
SALLE_T = 'salle_en_T'
SALLE_Y = 'salle_en_Y'

dictionnaire : Salle -> [ taille, type, nombre_personnes, dict Sorties -> (pos,debit), dict Sources -> (pos,debit)]

# positions :   Salle vide evident (Haut, Bas, Gauche, Droite) et composées
#               Salle de Classe : Bas (tableau), Haut(Fond de classe) et composées avec gauche et droite
#               Salle en T : Bas evident, Droite et Gauche pour les deux branches
#               Salle en Y : Comme T

pregeneration_debit( dictionnaire)
