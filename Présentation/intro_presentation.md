Intro :

Comme on a pu le constater dans les récents événements de la Grenfell Tower, à Londres, le pb posé par les incendies est toujours d'actualité. 
En effet, des normes pas assez strictes alliées à des mauvaises consignes d'évacuation on coûté la vie à plus de 70 personnes. L'établissement de normes plus strictes et de consignes d'évacuation optimisées semblent ainsi nécaissaires pour sauver des vies. Nous nous sommes intéressés, dans le cadre du TIPE, à l'optimisation des consignes d'évacuation, c'est à dire à l'établissement d'un plan d'évacuation incendie efficace.
Nous avons basé la recherche de ce plan d'évacuation optimal sur une modélisation du mouvement des personnes à l'intérieur du batiment concerné. L'approche la plus couremment utilisée consiste en la modélisation physique de ce mouvement. Cependant, le coût en ressource d'une telle modélisation à l'échelle d'un bâtiment entier est trop important pour notre matériel.
Nous avons donc séparé la modélisation en 2 parties. Une partie physique qui se concentre sur une échelle d'une salle, et une modélisation par flux à l'échelle du bâtiement.

Simulation locale :

Je vais vous présenter la simulation locale, donc je me suis occupé. Le but de la simulation est de renvoyer un débit réaliste exploitable pour la simulation globale.

Pour implémenter la simulation de façon simple et efficace, nous avons avons négligé certains paramètres. L'objctif du tipe n'est pas de gérer la physique du mouvement des personnes (déplacement, collisions...) . Nous avons utilisé une bibliothèque (Pymunk). 

Je vais maintenant expliquer comment on mondélise une salle :

La salle est représentée par 4 murs, et les sorties par des trous dans ces murs. On a d'abord modélisé les obstacles par des rectangles. Nous avons ensuite représenté les obstacles par des polygones convexes car cela nous laisse plus de liberté. Les agents sont représentés par des cercles.

Un point crucial de la modélisation est choisir le comportement des agents, à savoir la direction et la vitesse de leur déplacement.

Pour déplacer l'agent, on lui applique une force à l'aide du moteur physique. Pour rendre le déplacement vraisemblable, il faut trouver une direction permettant de contourner les obstacles.

Une première approche est le test de proximité. Pour cela on prend des points dans le voisinage de l'agent. On retire les points qui ne sont pas accessible par l'agent, et parmis les points restants, on sélectionne celui qui est le plus proche de la sortie. Ce point donne la direction à suivre de l'agent.
Dans cet exemple, ce point donne la direction de l'agent, qui n'est pas la direction la plus vraisemblable. 

On a donc pensé à une seconde approche, le lancer de rayons. Pour cela, on lance un rayon vers la sortie. Si aucun obstacle n'est rencontré, alors l'agent est dirigé vers la sortie, sinon, on choisis parmis les sommets accessibles de l'obstacle le sommet le plus proche du point d'impact.

Cette méthode est satisfaisante, mais ne fonctionne qu'avec des obstacles rectangulaires, on a donc cherché à la généraliser pour tout obstacle convexe, ce qui mène à notre choix d'utiliser une dichotomie.

Pour contourner correctement l'obstacle bloquant, nous avons considéré que les obstacles qui empêchent le contournement de cet obstacle ne forment qu'un. Cet obstacle et le mur sont considéré comme un seul et même obstacle, car on ne peut passer entre les deux.

On découpe la salle en 3 parties, dont un angle mort. On lance ensuite une dichotomie sur les 2 autres parties (bleu et violet), afin de trouver la direction qui permet de contourner l'obstacle.
On se retrouve avec 2 directions, une pour chaque zone. On rend la direction ayant l'angle le plus petit avec la sortie.
Les agens suivent un comportement réaliste, sauf dans un cas précis, lorsque les 2 angles sont quasiment égaux. Lorsque la personne prendra une direction, l'angle de l'autre direction diminuera, ce qui le poussera à choisir la direction opposée, et ainsi de suite. La personne sera donc coincée derrière le rang.
Ce problème a été grâce à des champs de vecteurs, mais je n'ai pas le temps de les décrire.

L'efficacité du choix du déplacement est dû à la structude de donnée utilisée par le moteur physique, qui est un arbe binaire qui découpe l'espace.

Pour atteindre une simulation plus réaliste, nous avons fait varier la vitesse en fonction du voisinage des agents. Nous avons donc appliqué la formule de Togawa, qui donne la vitesse en fonction de la densité de personnes autours de l'agent.

La modélisation ainsi implémentée nous a permis d'obtenir certains résultats. Tout d'abord, nous pouvons remarquer que les agents contournent les obstacles de façon vraisemblable.
Nous pouvons également remarquer que la dichotomie donne un comportement plus réaliste que le test de proximité.

A cause leur compétition pour sortir, les agents sont ralentis au niveau de la sortie. Une solution à ce problème communément admise par la littérature scientifique, et vérifiée expérimentalement, est de placer un obstacle devant la porte.
On a donc récupéré des débits moyens pour une salle vide, et une salle vide avec un obstacle devant la sortie. Les résultats obtenus vont à l'encontre des prévisions, ce qui rend compte des limites de notre simulation.

Néanmoins, la simulation reste globalement satisfaisante, et premet de renvoyer des
débits exploitables pour la simulation globale.

La simulation globale assigne les débits à chacune des transitions, et simule ainsi l'évacuation du bâtiment.

Conclusion Jean :


Thibault :

La simulation globale couplée à la simulation locale nous a permis de nous rendre compte que le plan du lycée est mal optimisé et présente des phénomènes d'engorgement. Il conviens cependant aux normes qui ne recherchent pas un plan optimal mais seulement un plan correspondant à 
 

