# Intro :

##Slide 1 
Comme on a pu le constater dans les récents événements de la Grenfell Tower, à Londres, le pb posé par les incendies est toujours d'actualité. 
En effet, des normes pas assez strictes alliées à des mauvaises consignes d'évacuation on coûté la vie à plus de 70 personnes. L'élaboration de normes plus strictes et de consignes d'évacuation optimisées semblent ainsi nécaissaires pour sauver des vies.

##Slide 2
Nous nous sommes intéressés, dans le cadre du TIPE, à l'optimisation des consignes d'évacuation, c'est à dire à l'établissement d'un plan d'évacuation incendie efficace.
Nous avons basé la recherche de ce plan d'évacuation optimal sur une modélisation du mouvement des personnes à l'intérieur du batiment concerné.

##Slide 3
L'approche la plus couremment utilisée consiste en la modélisation physique de ce mouvement. Cependant, le coût en ressource d'une telle modélisation à l'échelle d'un bâtiment entier est trop important pour notre matériel.

##Slide 4
Nous avons donc séparé la modélisation en 2 parties. Une partie physique qui se concentre sur une échelle d'une salle, et une modélisation par flux à l'échelle du bâtiement.

##Slide 5
Je vais vous présenter la simulation locale, dont je me suis occupé. Le but de la simulation est de renvoyer un débit réaliste exploitable pour la simulation globale.

#Slide 6
Pour implémenter la simulation de façon simple et efficace, nous avons négligé certains paramètres.

##Slide 7
L'objctif du tipe n'est pas de gérer la physique du mouvement des personnes (déplacement, collisions...) . Nous avons utilisé un moteur physque (Pymunk). 

##Slide 8 
Je vais maintenant expliquer comment on modélise une salle :

##Slide 9 - 12
La salle est représentée par 4 murs, et les sorties par des trous dans ces murs. On a d'abord modélisé les obstacles par des rectangles. Nous avons ensuite représenté les obstacles par des polygones convexes car cela nous laisse plus de liberté. Les agents sont représentés par des cercles.

##Slide 13 - 14
Un point crucial de la modélisation est choisir le comportement des agents, à savoir la direction et la vitesse de leur déplacement.

##Slide 15
Pour déplacer l'agent, on lui applique une force à l'aide du moteur physique. Pour rendre le déplacement vraisemblable, il faut trouver une direction permettant de contourner les obstacles.

##Slide 16
Une première approche a été uniquement de prendre en compte le voisinage proche de l'agent.

##Slide 17 - 20
Pour cela on prend des points dans le voisinage de l'agent. On retire les points qui ne sont pas accessible par l'agent, et parmis les points restants, on sélectionne celui qui est le plus proche de la sortie. Ce point donne la direction à suivre de l'agent.
Dans cet exemple, ce point donne la direction de l'agent, qui n'est pas la direction la plus vraisemblable. 

##Slide 21
On a donc pensé à une seconde approche,qui permet de rendre compte du champ de vision de l'agent. On peut ainsi espérer que cette approche donnera un comportement plus réaliste.

##Slide 22 - 23
Pour cela, on lance un rayon vers la sortie. Si aucun obstacle n'est rencontré, alors l'agent est dirigé vers la sortie. Sinon, on choisis parmis les sommets accessibles de l'obstacle le sommet le plus proche du point d'impact. (pointer les sommets accessibles)

##Slide 24
Cette méthode est satisfaisante, mais ne fonctionne qu'avec des obstacles rectangulaires, on a donc cherché à la généraliser pour tout obstacle convexe, ce qui mène à notre choix d'utiliser une dichotomie.

##Slide 25
Pour contourner correctement l'obstacle bloquant, nous considérons comme un seul et même objet l'obstacle bloquant et tout obstacle qui empêche le contournement de l'obstacle bloquant.
Cet obstacle et le mur sont considéré comme un seul et même obstacle, car on ne peut passer entre les deux. (pointer du doigt)

##Slide 26 - 28
Ensuite, on découpe la salle en 3 parties, dont un angle mort. Puis, on lance une dichotomie sur les angles dans les 2 autres parties (bleu et violet), afin de trouver la direction qui permet de contourner l'obstacle.

##Slide 29 - 30
On se retrouve avec 2 directions, une pour chaque zone. On prend la direction ayant l'angle le plus petit avec la sortie.

##Slide 31
Les agens suivent un comportement réaliste, sauf dans un cas précis, lorsque les 2 angles sont quasiment égaux. Lorsque la personne prendra une direction, l'angle de l'autre direction diminuera, ce qui le poussera à choisir la direction opposée, et ainsi de suite. La personne sera donc coincée derrière les 2 obstacles. (pointer)
Ce problème a été réglé grâce à des champs de vecteurs, mais je n'ai pas le temps de les décrire.

##Slide 32 - 33
L'efficacité du choix du déplacement est dû à la structude de donnée utilisée par le moteur physique, qui est un arbe binaire qui découpe l'espace.

##Slide 34 - 35
Pour atteindre une simulation plus réaliste, nous avons fait varier la vitesse en fonction du voisinage des agents.

##Slide 36
Nous avons donc appliqué la formule de Togawa, qui donne la vitesse en fonction de la densité de personnes autours de l'agent.

##Slide 37 - 38
La modélisation ainsi implémentée nous a permis d'obtenir certains résultats.

##Slide 39
Tout d'abord, nous pouvons remarquer que les agents contournent les obstacles de façon vraisemblable.

##Slide 40
Nous pouvons également remarquer que la dichotomie donne un comportement plus réaliste que le test de proximité.

##Slide 41
Nous nous sommes intéressés à un problème récurrent dans l'étude des mouvements de foule. A cause leur compétition pour sortir, les agents sont ralentis au niveau de la sortie. Une solution à ce problème communément admise par la littérature scientifique, et vérifiée expérimentalement, est de placer un obstacle devant la porte.

##Slide 42
On a donc récupéré des débits moyens pour une salle vide, et une salle vide avec un obstacle devant la sortie.

##Slide 43
Les résultats obtenus vont à l'encontre des prévisions, ce qui rend compte des limites de notre simulation. (expliquer l'histogramme)

##Slide 44
Néanmoins, la simulation reste satisfaisante, et premet de renvoyer des
débits exploitables pour la simulation globale.

##Slide 45 - 47
La simulation globale assigne les débits à chacune des transitions, et simule ainsi l'évacuation du bâtiment.

##Slide 48 (conclusion)

Notre simulation est imparfaite sur certains points, notemment sur les bases expérimentales qui auraient permis plus de réalisme. Cependant après quelques simulations sur le rez de chausser de nore lycée, nous avons pu nous rendre compte que le plan d'évacuation proposé par l'administration était loin d'être optimal car il présentait des phénomènes d'engorgement. Nous manqué temps pas renvoyer plan optimal.