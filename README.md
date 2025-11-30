(Ajouter boutons pour afficher phéromones et masquer le territoire non découvert)
(Chercher à remonter vers des phéromones plus anciens pour remonter une piste évantée. Par exemple: pour la descente de gradient, regarder uniquement dans la direction opposée au nest et choisir une cell dans cette direction.)
+ ( Pb: restent coincés aux frontières de l'environnement quand il y a des phéromones dessus)
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

a) TODO Comparison with full random
b) ~ graphs in interface
c) TODO fix dead ends near borders ("pheromones traps") = fix gradient descent
d) TODO add possibilities in config_w: quantité clusters & food
e) "OK" interface plus user friendly
f) PDF CR, focus on gradient descent and decentralised knowledge