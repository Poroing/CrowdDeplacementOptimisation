<!-- vim: set spell spelllang=fr: -->

# Crowd Simulation for Emergency Response Planning

Pour désigner les personnes on utilise le terme "agent" (Pourrions nous utiliser
cela dans nos programmes et notre présentation?)

Il est dangereux d'embaucher tout une foule pour tester les sécurité d'un bâtiment
et c'est aussi très cher. d'où la simulation.

Prends en compte plusieurs paramètres dont la panique et les liens familiaux
(Peut être expliquer pourquoi on n'utilise pas un niveau de panique ou en implémenter un,
pas si compliquer pour certaine partie, nécessite certaine modification prévus pour d'autre)

Une foule peut être représenté par des particule ce qui prend en compte la tendance d'un
individu à suivre la foule et à s'éloigner des autres individus, mais parfois
les agents peuvent se comporter autrement qu'un individu comme en essayant de s'éloigne
de la sortie.

Il parle d'automate cellulaire, mais bon, il n'y a pas l'aire d'avoir grand chose d'intéressant
juste ce que l'on s'attendrai d'un automate cellulaire

Le système de simulation dominant est la simulation de chaque agent individuellement c'est la
simulation qu'il a choisie

Simulation fait en 2D car plus simple pour les calcule de collision et de recherche de chemin
(J'ai pas de vocabulaire) Bâtiment sur plusieurs niveau impossible (Intéressant d'en parler)

Il donne des attribut à chacune des personnes comme la panique

Le choix du parcours se fait récursivement en regardant si il y a un obstacle dans le chemin vers
la sortie et si cette obstacle peut être contourné

Pour choisir un chemin il prends en compte le nombre de personnes sur ce chemin

Les personnes ne sont pas considérer comme des obstacle car ils peuvent bouger et lorsqu'une
personne arrive à moins d'un mètre d'une personne il essaie de la contourner

Le point important de la simulation est l'implémentation de groupe dirigé par des chefs

L'implémentation des groupes marche bien

n'as pas réussi à simuler l'espace que les personnes ont besoin autour d'eux
