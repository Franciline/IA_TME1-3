import numpy as np
from typing import Tuple

def matriceCE(fichier: str) -> list:
    """
    Matrice de préférences des étudiants pour les parcours à partir d'un fichier txt.

    Parameters
    ----------
        fichier : fichier txt à lire
    Returns
    -------
        list[list[int]] : matrice de taille nb étudiant x nb de parcours, une sous-liste list[i] représente
                        les préférences de l'étudiant i par ordre croissant
    """

    monFichier = open(fichier, "r")     # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines()    # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne
    monFichier.close()  # Fermeture du fichier

    nbEtu = int(contenu[0])
    matrice = [[int(x) for x in contenu[i+1].split()[2:]] for i in range(nbEtu)]

    return matrice

def matriceCP(fichier: str) -> list:
    """
    Matrice de préférences des parcours pour les étudiants à partir d'un fichier txt.

    Parameters
    ----------
        fichier : fichier txt à lire
    Returns
    -------
        list[list[int]] : matrice de taille nb de parcours x nb étudiant, une sous-liste list[i] représente
                        les préférences du parcours i par ordre croissant
    """
    monFichier = open(fichier, "r")     # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines()    # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne
    monFichier.close()  # Fermeture du fichier

    nbParcours = len(contenu) - 2       # except deux premieres lignes
    capacites = [int(cap) for cap in contenu[1][3:].split()]
    matrice = [[int(x) for x in contenu[i+2].split()[2:]] for i in range(nbParcours)]

    return capacites, matrice

def genMatriceCE(n: int)-> list:
    """
    Génère aléatoirement la matrice de préférences des n étudiants pour les 9 parcours.

    Parameters
    ----------
        n: le nombre d'étudiants
    Returns
    -------
        list[list[int]] : matrice de taille 9 x n, une sous-liste list[i] représente
                        les préférences de l'étudiant i par ordre croissant    
    """
    # génération aléatoire des préférences, passage par numpy pour shuffle
    matriceCE = np.array([[x for x in range(9)] for _ in range(n)])
    [np.random.shuffle(row) for row in matriceCE]
    
    return np.ndarray.tolist(matriceCE)


def genMatriceCP(n: int)-> list:
    """
    Génère aléatoirement la matrice de préférences des 9 parcours pour les n étudiants.

    Parameters
    ----------
        n: le nombre d'étudiants
    Returns
    -------
        list[list[int]] : matrice de taille 9 x n, une sous-liste list[i] représente
                        les préférences du parcours i par ordre croissant    
    """
    # génération aléatoire des préférences, passage par numpy pour shuffle
    matriceCP = np.array([[x for x in range(n)] for _ in range(9)])
    [np.random.shuffle(row) for row in matriceCP]
    
    return np.ndarray.tolist(matriceCP)


def genCapacite(n: int)->list:
    """
    Génère aléatoirement des capacités de façon équilibré pour les 9 parcours telle que cela somme à n.

    Parameters
    ----------
        n: le nombre d'étudiants
    Returns
    -------
        list: la liste des capacités pour chaque parcours   
    """
    # répartition a peu près équilibré
    cap = [n // 9 for _ in range(9)]
    for _ in range(n % 9):
        cap[np.random.randint(0, 9)] += 1 # ajout à des parcours aléatoires

    return cap


def matrices_utilite(fichierCE: str, fichierCP: str) -> Tuple[list, list, list, list]:
    """
    Renvoie la matrice des utilités pour les étudiants, pour les parcours
    et la somme correspondante de ces deux matrices

    Parameters
    -----------
        fichierCE: nom du fichier contenant les préférences des étudiants (row etudiant, col parcours)
        fichierCCP: nom du fichier contenant les préférences des parcours (row parcours, col étudiants)

    Returns
    -------
    caps: capacité des parcours
    score_parc: matrice des utilités des étudiants
    sorted_etud: matrice des utilités des parcours
    utility_mat: matrice = score_parc + sorted_etud.T
    """
    util_etud = matriceCE(fichierCE)    
    caps, util_parc = matriceCP(fichierCP)    

    # on associe à chaque parcours leur score borda: pour chaque elements x_pe = [num_parc/etud, score borda]
    # tri en fonction des numéros d'étudiants -> sorted_parc[3][0] = score borda de etud 0 pour parc 3 
    sorted_parc = [sorted([[row[i], len(row) - i - 1] for i in range(len(row))], key=lambda x: x[0]) for row in util_parc]
    sorted_etud = [sorted([[row[i], len(row) - i - 1] for i in range(len(row))], key=lambda x: x[0]) for row in util_etud]
    
    # garder le score uniquement : [num_parc/etud, score borda] -> [score borda]
    sorted_parc = [[row[i][1] for i in range(len(row))] for row in sorted_parc]
    sorted_etud = [[row[i][1] for i in range(len(row))] for row in sorted_etud]

    utility_mat = list(np.array(sorted_parc) + np.array(sorted_etud).T) # matrice d'utilité

    return caps, sorted_parc, sorted_etud, utility_mat