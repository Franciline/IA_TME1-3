import gurobipy as gp
from gurobipy import GRB
import numpy as np
from matrice_pref import matrices_utilite

# Q14 maximiser les utilités

NBPARCOURS, NBETUDIANTS = 9, 11

folder = "preferences_data"
caps, sorted_parc, sorted_etud, utility_mat = matrices_utilite(f"{folder}/PrefEtu.txt", f"{folder}/PrefSpe.txt")

# Create a new model
model = gp.Model('Q14')

# ajout variables
x = model.addVars(NBPARCOURS, NBETUDIANTS, vtype=GRB.BINARY, name="x")

# Constraints on capacity
model.addConstrs(gp.quicksum(x[i, j] for j in range(NBETUDIANTS)) == caps[i] for i in range(NBPARCOURS))
# Constraints on max 1 master
model.addConstrs((gp.quicksum(x[i, j] for i in range(NBPARCOURS)) == 1 for j in range(NBETUDIANTS)))

# objective
model.setObjective(gp.quicksum(x[i, j] * utility_mat[i][j] for i in range(NBPARCOURS)
                               for j in range(NBETUDIANTS)), GRB.MAXIMIZE)

model.optimize()
model.write("plne/plne_q14.lp")
print(model.status)


print("\nVariables x_pe à 1, utilité parcours, utilité étudiant, utilité totale\n")
total_u_parc, total_u_etud = 0, 0
min_et, min_parc = NBPARCOURS, NBETUDIANTS  # seuil borda

for v in model.getVars():
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
