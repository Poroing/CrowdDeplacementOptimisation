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

# Crown Simulation Modeling Applied to Emergency and Evacuation Simulatons using Multi-Agent Systems

L'étude des foules a toujours était fait avec du matériel réel par des sociologue ce qui n'est pas correcte
car les personne ne sont pas souvent paniqué lors de ces études

Les personnes ont tendance à prendre le chemin le plus cours même si il y a beaucoup de gens dans le cas
où ils ne sont pas paniqué  (Conflit avec le papier précédent qui est moins sérieux) "Least effort principle"

Ces situations disparaisse lorsqu'il y a panique ou lorsque les personne cherches la meilleure place assise
dans un concert ou pour les achat (Des domaines d'application supplémentaire) Ils ne font plus attention
à leurs distance avec les autres et prennent le seul chemin qu'il connaisse pour sortir lorsqu'il ne
connaisse pas de chemin pour sortir

Les personnes ont tendance à suivre un autre groupe de personne en pensant qu'il pourront les sortir de
la situation dangereuse, ce genre de disposition ne permet pas une évacuation optimal

Les tas de gens devant les portes s'appel "arching" (Je sais pas comment le dire en Français)

trois raisons pour une simulation, tester des théorie scientifique et hypothèse, tester les
stratégies de sécurité, déduire des études théoriques

On peut utiliser des rapport historiques

Les foules ne peuvent être simulé facilement avec des équations

On peut faire des modélisation par un graphe appelé modèle macroscopique

Automate cellulaire peut être utilisé pour une étude microscopique comme macroscopique mais ne
peux simuler le mouvement erratique des agents surtout utiliser pour les jeux 

Le truc d'Alex s'appelle Flow-based system, et le notre Multi-agent system

Les système multi-agent sont les plus réaliste SIMULEX fut le premier 

La grande complexité des MAS demandant beaucoup de donnée et de temps de processeur
à créé des difficulté malgré la loi de Moore, mais MAS donne beaucoup de possibilité
tant que les donnée sur le comportement individuelle est correctement fournie

Le modèle MAS modélise le mouvement d'un agent et étudie le comportement de la foule
qu'il en émerge
