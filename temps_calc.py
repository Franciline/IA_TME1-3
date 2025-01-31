from gale_shapley import gale_shapley_etud, gale_shapley_parc
from matrice_pref import genMatriceCE, genMatriceCP, genCapacite
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Callable

# Partie 2


def plotting(x: list, y: list, xlabel: str, ylabel: str, title: str):
    """
    Affiche le graphe pour les valeurs x et y.

    Parameters
    ----------
        x: liste des valeurs en abscisse 
        y: liste des valeurs en ordonnée
        xlabel: titre axe x
        ylabel: titre axe y
        title: titre du graphique
    """

    data = pd.DataFrame(list(zip(x, y)))
    data.columns = [xlabel, ylabel]
    sns.set_theme(font_scale=1.40)
    axes = sns.lineplot(data=data, x=xlabel, y=ylabel)
    axes.set_title(title, fontsize=20)

    # affichage de certaines valeurs de x
    for ind, label in enumerate(axes.get_xticklabels()):
        if ind % 4 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    label.set_visible(True)
    plt.show()


def plot_temps(debut: int, fin: int, pas: int, nb: int, gale_shapley: Callable):
    """
    Calculer le temps de calcul en moyenne en fonction du n tests de la fonction Gale-Shapley pour le nombre 
    d'étudiants variant de [debut, fin] avec un pas donné. Trace ensuite la courbe associée avec le nombre d'étudiants 
    sur l'axe des X et le temps du calcul sur l'axe des Y.

    Parameters
    ----------
        debut: int
            valeur de départ
        fin: int
            valeur de fin
        pas: int 
            le pas 
        nb: int
            nombre de tests pour chaque itérations
        gale_shapley: Callable 
            la fonction qui implémente l'algorithme de Gale-Shapley étudiants ou parcours optimal.
    """

    res = []

    for nbEtu in range(debut, fin+1, pas):
        matCE, matCP = genMatriceCE(nbEtu), genMatriceCP(nbEtu)  # génération aléatoire des matrices de préférence
        capacite = genCapacite(nbEtu)  # génération de la capacité

        temps = 0

        for _ in range(nb):
            start = time.time()
            _ = gale_shapley(matCE, matCP, capacite)
            temps += time.time() - start
        res.append(temps/nb)

    x = [str(x) for x in range(debut, fin+1, pas)]

    plotting(x, res, "nombre d'étudiants", "temps de calcul (sec)", "Temps de calcul en fonction du nombre d'étudiants")


def plot_nb_iter(debut: int, fin: int, pas: int, gale_shapley: Callable):
    """
    Calcul le nombre d'itérations temps de calcul en moyenne sur n tests de la fonction Gale-Shapley pour le nombre 
    d'étudiants variant de [debut, fin] avec un pas donné. Trace ensuite la courbe associée.

    Parameters
    ----------
        debut: int 
            valeur de départ
        fin: int 
            valeur de fin
        pas: int 
            le pas 
        gale_shapley : Callable
            la fonction qui implémente l'algorithme de Gale-Shapley étudiants ou parcours optimal
    """

    res = []

    for nbEtu in range(debut, fin+1, pas):
        matCE, matCP = genMatriceCE(nbEtu), genMatriceCP(nbEtu)  # génération aléatoire des matrices de préférence
        capacite = genCapacite(nbEtu)  # génération de la capacité

        _, nb_iter = gale_shapley(matCE, matCP, capacite)
        res.append(nb_iter)

    x = [str(x) for x in range(debut, fin+1, pas)]

    plotting(x, res, "nombre d'étudiants", "nombre d'itérations",
             "Nombre d'itérations en fonction du nombre d'étudiants")


if __name__ == '__main__':
    plot_temps(200, 5000, 200, 10, gale_shapley_parc)  # put in ipynb
    # plot_nb_iter(200, 5000, 200, gale_shapley_parc)  # put in ipynb
