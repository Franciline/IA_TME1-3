import gurobipy as gp
from gurobipy import GRB
import numpy as np
from matrice_pref import matriceCE, matriceCP

nbparc, nbetud = 9, 11
util_etud = matriceCE("PrefEtu.txt")
caps, util_parc = matriceCP("PrefSpe.txt")

# on associe à chaque parcours leur score borda
# pour chaque elements x_pe: [num_parc/etud, score borda]
score_etud = [[[row[i], len(row) - i - 1] for i in range(len(row))] for row in util_etud] 
score_parc = [[[row[i], len(row) - i - 1] for i in range(len(row))] for row in util_parc] 

# tri en fonction des numéros d'étudiants -> sorted_parc[3][0] = score borda de etud 0 pour parc 3 
sorted_parc = [sorted([[row[i], len(row) - i - 1] for i in range(len(row))], key=lambda x: x[0]) for row in util_parc]
sorted_etud = [sorted([[row[i], len(row) - i - 1] for i in range(len(row))], key=lambda x: x[0]) for row in util_etud]

# only get the scores : [num_parc/etud, score borda] -> [score borda]
sorted_parc = [[row[i][1] for i in range(len(row))] for row in sorted_parc]
sorted_etud = [[row[i][1] for i in range(len(row))] for row in sorted_etud]

utility_mat = list(np.array(sorted_parc) + np.array(sorted_etud).T) # matrice d'utilité

# Create a new model
model = gp.Model('Q14')

# ajout variables
x = model.addVars(nbparc, nbetud, vtype=GRB.BINARY, name="x")

# Constraints on capacity
model.addConstrs(gp.quicksum(x[i, j] for j in range(nbetud)) == caps[i] for i in range(nbparc))
# Constraints on max 1 master
model.addConstrs((gp.quicksum(x[i, j] for i in range(nbparc)) == 1 for j in range(nbetud)))

# objective 
model.setObjective(gp.quicksum(x[i, j] * utility_mat[i][j] for i in range(nbparc)
              for j in range(nbetud)), GRB.MAXIMIZE)

model.optimize()
model.write("q14.lp")
print(model.status)

# affichage

print("\nVariables à 1")
total_u_parc, total_u_etud = 0, 0
min_et, min_parc = nbparc, nbetud #seuil borda

for v in model.getVars():
    if v.X > 0:
        index = list(map(int, v.VarName.strip('x[]').split(',')))
        p, e = index[0], index[1]

        #set mean
        total_u_parc += sorted_parc[p][e]
        total_u_etud += sorted_etud[e][p]

        #set min
        if min_parc > sorted_parc[p][e]:
            min_parc = sorted_parc[p][e]

        if min_et > sorted_etud[e][p]:
            min_et = sorted_etud[e][p]

        print(f"{v.VarName}  \tU(p{p})={sorted_parc[p][e]}  \tU(e{e})={sorted_etud[e][p]}  \ttotal {utility_mat[p][e]}")

print(f"\nMoyenne utilité parcours {np.round(total_u_parc/nbetud, 2)}\nUtilité min parcours {min_parc}")
print(f"\nMoyenne utilité étudiants {np.round(total_u_etud/nbetud, 2)}\nUtilité min étudiants {min_et}")
print(f"\nMoyenne utilité totale {np.round((total_u_parc + total_u_etud)/(2*nbetud), 2)}")
