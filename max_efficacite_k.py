import gurobipy as gp
from gurobipy import GRB
import numpy as np
from scipy.sparse import csr_array
from matrice_pref import matriceCE, matrices_utilite

NBPARCOURS, NBETUDIANTS = 9, 11
k = 5

folder = "preferences_data"
util_etud = matriceCE(f"{folder}/PrefEtu.txt")
caps, sorted_parc, sorted_etud, utility_mat = matrices_utilite(f"{folder}/PrefEtu.txt", f"{folder}/PrefSpe.txt")

# dictionnaire k chaque parcours on associe les étudiants qui l'ont en k premier
dict_k = {x: [] for x in range(NBPARCOURS)}
for numEtu in range(NBETUDIANTS):
    for i in range(k):
        dict_k[util_etud[numEtu][i]].append(numEtu)  # ajout étudiant dans ce parcours

rows = [key for key in dict_k.keys() for _ in range(len(dict_k[key]))]
cols = [stud for studs in dict_k.values() for stud in studs]

matrix = csr_array(([1] * len(rows), (rows, cols)), shape=(NBPARCOURS, NBETUDIANTS), dtype=int)

m = gp.Model("q15")

# Ajouter uniquement les contraintes nécessaires
x = m.addVars(((p, s) for p in range(NBPARCOURS)
              for s in range(NBETUDIANTS) if matrix[p, s] > 0), vtype=GRB.BINARY, name="x")  # ajout x_pe si vérifie k*

valid_parcours = {p for p, _ in x.keys()}
valid_etudiants = {e for _, e in x.keys()}


# Contraintes sur les capacités des parcours
m.addConstrs((gp.quicksum(x[i, j] for j in dict_k[i]) == caps[i] for i in dict_k.keys() if dict_k[i]))

# Contraintes que chaque étudiant doit être affecté à au plus 1 parcours
m.addConstrs((gp.quicksum(x[p, j] for p in [p for (p, e) in x.keys() if e == j]) == 1 for j in valid_etudiants))


# Fonction objective : maximiser la somme des utilités pour les étudiatns ayant leur k premiers choix
m.setObjective(gp.quicksum(x[i, j]*utility_mat[i][j] for (i, j) in x.keys() if matrix[i, j] > 0), GRB.MAXIMIZE)

m.optimize()
m.write("plne/plne_q15.lp")
print(m.status)

total_u_parc, total_u_etud = 0, 0
min_et, min_parc = NBPARCOURS, NBETUDIANTS  # seuil borda

for k, v in dict_k.items():
    print(k, v)

for v in m.getVars():
    if v.X > 0:
        index = list(map(int, v.VarName.strip('x[]').split(',')))
        p, e = index[0], index[1]

        # set mean
        total_u_parc += sorted_parc[p][e]
        total_u_etud += sorted_etud[e][p]

        # set min
        if min_parc > sorted_parc[p][e]:
            min_parc = sorted_parc[p][e]

        if min_et > sorted_etud[e][p]:
            min_et = sorted_etud[e][p]

        print(f"{v.VarName}  \tU(p{p})={sorted_parc[p][e]}  \tU(e{e})={sorted_etud[e][p]}  \ttotal {utility_mat[p][e]}")

print(f"\nMoyenne utilité parcours {np.round(total_u_parc/NBETUDIANTS, 2)}\nUtilité min parcours {min_parc}")
print(f"\nMoyenne utilité étudiants {np.round(total_u_etud/NBETUDIANTS, 2)}\nUtilité min étudiants {min_et}")
print(f"\nMoyenne utilité totale {np.round((total_u_parc + total_u_etud)/(2*NBETUDIANTS), 2)}")
