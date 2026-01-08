(Ajouter boutons pour afficher phéromones et masquer le territoire non découvert)
(Chercher à remonter vers des phéromones plus anciens pour remonter une piste évantée. Par exemple: pour la descente de gradient, regarder uniquement dans la direction opposée au nest et choisir une cell dans cette direction.)
(Reset the memory of ants when back at the nest? Forget gradually? Evaporate in the memory?)
(Compute the minimal solution = shortest path from nest to food while avoiding obstacles for every food unit)
+ ( Pb: restent coincés aux frontières de l'environnement quand il y a des phéromones dessus)
+ ( Pb: Bug2 stuck in obstacles clusters sometimes)
1) PheromoneMap
2) Collect of Food strategy
3) Pheromones induced movement
4) Interface:
    - OK Quantité de units de food récupérés sur le total OK
    - afficher le terrain visité en blanc ou pas
    - afficher les phéromones ou pas
    - OK durée en ms en direct OK
    - OK durée pour ramasser tout le food
    - graphe dynamique du nombre de food en fonction du temps + nb food/quantité de phéromones déversée en fonction du tps?
    - légende
    - comparer les résultats avec du full aléatoire (afficher une autre fenêtre à côté pour le même environnement mais du full aléatoire)
    - comparaison to ACO algo limitée puisqu'une fourmi retourne au nest immédiatement après avoir récolté un unit de food Voir article sur dynamic ACO
    - OK modifier paramètres de config (pheromones characteristics and ant quantity)
    - OK le nombre de déplacements de toutes les fourmis

a) TODO: Comparison with full random
b) ~ graphs in interface
c) OK fix dead ends near borders ("pheromones traps")
d) TODO: add possibilities in config_w: quantité clusters & food
e) "OK" interface plus user friendly
f) PDF CR, focus on gradient descent and decentralised knowledge

TRY WITHOUT OBSTACLES PARCE QUE C'EST UN AUTRE PROBLEME!!!

A) PHEROMONE TRAPS
- pondérer la direction du déplacement avec des paramètres choisis tels que la case choisie dépend à la fois : de l'aléatoire, des phéromones, de la distance au nid
    + permettre de modifier le rapport aléatoire/phéromones avec un curseur en direct dans l'interface graphique (donc: avoir une interface graphique en direct). Curseur de aléatoire pur à ce que j'ai maintenant = 1st report stage.
- Part of it is due to wrong pheromone diffusion at the borders: the pheromones spreading out of the border should still diffuse inside of the environment and vice-versa
    1) OK (maybe: no theory...) Fix the pheromones diffusion
    2) TODO: Add the random/pheromones cursor on the interface (and consider that the problem shall be tackled later and that we will use large environments because to find the answer I might have to know whether there is always an optimal solution (or whatever something like this) )
    2bis) TODO: Interface (nice one like seen before) = More parameters at the beginning + generate another one with live data when the parameters are set, with some dynamic parameters that we can change during the simulation.
    3) TODO: Répondre à la question de Paul dans le rapport et la présentation avec un calcul de compléxité etc.: c'est une question de théorie, pas forcément de programmation donc voir à quel point il faut s'intéresser à la question.
    4) OK Add a minimum threshold for pheromones attraction


I consider two ways to improve the efficiency of the ants to bring food to their nest:
- one is to follow pheromone trails "wisely" and so to optimize the exploration algorithm;
- conjointly, the other is to spread pheromones relevently and so to optimize the way back from the food source to the ant nest.
The exploration part will be focused in comparing the efficiency of my algorithm with a random search, while the obstacle avoidance optimization part would consist in searching for the most efficient algorithm to avoid clusters of obstacles. As my project is focused on the ant optimization, I will first focus on providing the relevant feedback to assess the efficiency of my algorithm, while displaying no obstacle in the environment. Then, I might research what is the best algorithm to avoid clusters of obstacles and implement it. Nevertheless, those are too different problems related to objects located in clusters which should be adressed separately.

- average distance on the last few ants, walked by ants on a food trip from nest to nest, with only one cluster of food (otherwise the value is not relevant)
- distance walked by the ants seems weird
CHANTIER!!!!! Changer la def de env et ants après le choix des paramètres et donc afficher l'environnement uniquement après qu'ils aient été confirmés