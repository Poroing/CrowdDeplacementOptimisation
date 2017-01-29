Alex présente la nécessité d'une solution pour déterminer les débits
qui sont beaucoups trops impératif

On présente alors la simulation locale avec ses charactéristiques
	- c'est une simulation physique et non mathématique
	- On utilise une bibliothèque python pour se concentrer sur le traitement
	de donnée et l'intelligence des personnes

Les personnes
	- On a représenté les personnes par des cercles d'un rayon approximatif 40 cm
	- On les anime d'un force qui les mène à l'entrée
	- Il se trouve que dans une salle, il y a des obstacle, les gens doivent éviter les obstacles (principalement les rangs)
	- On a d'abord essayé de faire une intelligence locale, c'est à dire
	les gens regardent dans leur proximité mais cela n'est pas très réaliste car les gens
	ont tendance
	- On a trouvé une meilleure solution grâce un papier sur la modélisation sur la réponse
	d'une foule en cas d'urgence
	- Cela consiste en un lancer de rayon (BESOIN DIAPO)
	- Il faut prendre en compte les problème la place sur le côté

On a ainsi une simulation sur laquelle on peut récuperer des donneés

	- On récupère les valeurs lors de la sortie des gens
	- On veut un débit, il y a nécessité de dérivé
	- Si on fait ça basiquement, c'est pas très représentatif
	- On cherche à lisser la courbe

Qu'est ce que l'on peut faire par la suite --> beaucoup de choses

