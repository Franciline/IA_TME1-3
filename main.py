#import exemple  # Pour pouvoir utiliser les methodes de exemple.py
# Q1
from gale_shapley import gale_shapley_etud, gale_shapley_parc

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


if __name__ == '__main__':
    matCEtu = matriceCE("PrefEtu.txt")
    cap, matCParc = matriceCP("PrefSpe.txt")
    print("Etudiant optimal : ",gale_shapley_etud(matCEtu, matCParc, cap))
    print("Parcours optimal : ",gale_shapley_parc(matCEtu, matCParc, cap))