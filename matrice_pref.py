import numpy as np

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