#import exemple  # Pour pouvoir utiliser les methodes de exemple.py
# Q1
from gale_shapley import gale_shapley_etud, gale_shapley_parc
from matrice_pref import matriceCE, matriceCP, genMatriceCE, genMatriceCP, genCapacite


if __name__ == '__main__':
    matCE = matriceCE("PrefEtu.txt")
    cap, matCParc = matriceCP("PrefSpe.txt")
    print("Etudiant optimal : ",gale_shapley_etud(matCE, matCParc, cap))
    print("Parcours optimal : ",gale_shapley_parc(matCE, matCParc, cap))
    print("Matrice CE aléatoire :",genMatriceCE(5))
    print("Matrice CP aléatoire :",genMatriceCP(5))
    