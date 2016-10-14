# Travail à faire
- Implémenter un graphe orienté pour modéliser les mouvement lors d'un incendie (Alex)
- Implémenter une simulation de mouvement de foule applicable pour un mouvement  (les autres)
 de foule pendant un incendie

# Subtilité
- Prendre en compte le mental des gens
- Savoir que le mot départagement n'existe pas et qu'on dit juste 'Partage des taches'

## Simulation
1. Implémenter à l'aide d'objet une base de code permettant de
 coupler la physique (Pymunk) et l'affichage (Pygame) pour ainsi
 faciliter le travail sur la simulation

2. Modéliser la salle 
	1.  Faire un objet représentant un mur 
		1. [1?] incorporer la physique de façon intelligente
	2. Faire un objet représentant une sortie 
	3. [2.1, 2.2] Coupler l'objet mur et sortie pour définir la salle  
	4. [2.2] Définir une interface pour donner les sorties aux Personnes
	5. Faciliter l'ajout de polygone quelconque dans la salle

3.  Modéliser le comportement des Personnes
	1. Gérer le déplacement des Personnes
		1. [2.2] Déterminer la direction de déplacement en fonction des sorties
		2. Gérer l'interaction des personnes avec les autres personnes

4. Créer une interface pour le couplage avec le graphe
