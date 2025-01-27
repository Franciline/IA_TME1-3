from gale_shapley import gale_shapley_etud, gale_shapley_parc
from matrice_pref import genMatriceCE, genMatriceCP, genCapacite
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    sns.set_theme()
    sns.lineplot(data=data, x=xlabel,y=ylabel).set_title(title)
    plt.show()

def test_calc(debut: int, fin: int, pas: int, nb: int):
    """
    Test le temps de calcul en moyenne sur n tests de la fonction Gale-Shapley pour le nombre 
    d'étudiants variant de [debut, fin] avec un pas donné. Trace ensuite la courbe associée.

    Parameters
    ----------
    debut: valeur de départ
    fin: valeur de fin
    pas: le pas 
    nb: nombre de tests pour chaque itérations
    """
    res = []

    for nbEtu in range(debut, fin+1, pas):
        matCE, matCP = genMatriceCE(nbEtu), genMatriceCP(nbEtu) # génération aléatoire des matrices de préférence
        capacite = genCapacite(nbEtu) # génération de la capacité

        temps = 0

        for _ in range(nb):
            start = time.time()
            _ = gale_shapley_parc(matCE, matCP, capacite) # ? which gale shapley side not precised
            temps += time.time() - start
        res.append(temps/nb)

    x = [str(x) for x in range(debut, fin, pas)]

    plotting(x, res, "n", "temps de calcul (sec)", "temps de calcul en fonction de n")
        
if __name__ == '__main__':
    test_calc(200, 5000, 300, 10) # put in ipynb 
    