from gale_shapley import gale_shapley_etud, gale_shapley_parc
from matrice_pref import matriceCE, matriceCP, genMatriceCE, genMatriceCP, genCapacite
import time

# Partie 2

if __name__ == '__main__':
    # Temps de calcul
    nb_test = 10
    res = []

    for n in range(200, 2200, 200):
        matCE, matCP = genMatriceCE(n), genMatriceCP(n)
        cap = genCapacite(n)

        # 10 tests minimum
        sum_time = 0

        for _ in range(nb_test):
            start = time.time()
            gale_shapley_etud(matCE, matCP, cap)
            sum_time += time.time() - start
        
        res.append(sum_time/nb_test)
    print(res)
        