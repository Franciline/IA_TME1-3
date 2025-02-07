# IA_TME1-3

**Tests**

- Le fichier `tests.ipynb` est un Jupyter notebook qui les résultats des fonctions implémentées ainsi que quelques tests sur les données données.

**Script Python**

- `exemple.py` a été fournie au début du projet.

1. Partie 1. Gale-Shapley

- `gale_shapley.py` contient les algorithmes de Gale-Shapley ainsi que la fonction qui permet de retrouver les paires instables.
- `matrice_pref.py` contient les fonctions que manipulent des matrices. Elles permettent
- - de créer les matrices de préférences à partir du format donné par des fichiers `PrefEtu.txt` et `PrefSpe.txt`.
- - de générer les capacités aléatoire (voir Partie 2).
- - de générer la matrice d'utilité (voir Partie 3).

2. Partie 2. Temps du calcul et nombre d'itérations pour Gale-Shapley

- `plot.py` contient le code nécessaire pour calculer le temps du calcul / nombre d'itérations et générer des graphiques correspondants.

3. Partie 3. PL(NE)
   Le dans les fichiers suivants est adapté uniquement pour les données données par les fichiers `PrefEtu.txt` et `PrefSpe.txt`.

- `plne_k.py` permet de construire le modèle pour résoudre le problème linéaire de trouver la solution équitable pour les étudiants. Le problème est résolu en trouvant `k` tel qu'il existe la solution parfaite pour les étudiantes.
- `max_efficacite_k.py` permet de construire le modèle pour résoudre le problème linéaire de trouver la solution efficace pour les parcours et pour les étudiants pour k = 5.
- `max_efficacite_k.py` permet de construire le modèle pour résoudre le problème linéaire de trouver la solution efficace pour les parcours et pour les étudiants pour k = nombre des étudiants.

Chaque fichier génère le fichier `.lp` avec le problème linéaire formulé.

**Dossiers**

- Le dossier `plne` contient tous les fichieres `.lp` générés.
- Le dossier `preferences_data` contient les fichiers fournis sur les préférences des étudiants et des parcours.
