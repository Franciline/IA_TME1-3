import exemple # Pour pouvoir utiliser les methodes de exemple.py

# Q1
def matriceCE(fichier : str) -> list:
    """
    matrice de preference pour les étudiants
    """

    monFichier = open(fichier, "r")     # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines()    # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close()                  #Fermeture du fichier

    nbEtu = int(contenu[0])
    matrice = [[int(x) for x in contenu[i+1].split()[2:]] for i in range(nbEtu)]

    return matrice

def matriceCP(fichier: str) -> list:
    """
    matrice de préférence des parcours
    """
    monFichier = open(fichier, "r")     # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines()    # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close()                  #Fermeture du fichier

    nbParcours = len(contenu) - 2       # except deux premieres lignes
    matrice = [[int(x) for x in contenu[i+2].split()[2:]] for i in range(nbParcours)]
    
    return matrice



if __name__ == '__main__':
    matCEtu = matriceCE("PrefEtu.txt")
    matCParc = matriceCP("PrefSpe.txt")

    print(matCEtu,"aaah \n", matCParc)
