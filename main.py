# import exemple  # Pour pouvoir utiliser les methodes de exemple.py
# Q1
from gale_shapley import gale_shapley_etud, gale_shapley_parc, get_instable
from matrice_pref import matriceCE, matriceCP, genMatriceCE, genMatriceCP, genCapacite


if __name__ == '__main__':
    matCE = matriceCE("PrefEtu.txt")
    cap, matCParc = matriceCP("PrefSpe.txt")

    optim_etud, _ = gale_shapley_etud(matCE, matCParc, cap)
    optim_parc, _ = gale_shapley_parc(matCE, matCParc, cap)
    print("Etudiant optimal : ", optim_etud)
    print("Parcours optimal : ", optim_parc)
    print("Paires instables :", get_instable(matCE, matCParc, optim_etud))
    print("Matrice CE aléatoire :", genMatriceCE(5))
    print("Matrice CP aléatoire :", genMatriceCP(5))
