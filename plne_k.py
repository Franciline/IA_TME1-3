import gurobipy as gp
from gurobipy import GRB
import numpy as np
from scipy.sparse import csr_array

nparcours, netudiants = 9, 11  # rows = parcours, column = etudiants
# Capacités des parcours
caps = [2, 1, 1, 1, 1, 1, 1, 1, 2]

# k = 3
# parcours = {0: [5, 7],
#             1: [],
#             2: [9],
#             3: [],
#             4: [10],
#             5: [0, 1, 3],
#             6: [0, 1, 3],
#             7: [6, 7],
#             8: []}

# # k = 8
# parcours = {0: [0, 1, 3, 4, 5, 7, 10],
#             1: [0, 1, 3, 4, 5, 7, 9, 10],
#             2: [0, 1, 3, 4, 5, 7, 9],
#             3: [0, 1, 3, 4, 5, 6, 7, 9],
#             4: [3, 4, 5, 7, 10],
#             5: [0, 1, 3, 4, 6],
#             6: [0, 1, 2, 3, 4, 5, 6, 7],
#             7: [0, 1, 3, 4, 5, 6, 7, 9],
#             8: [0, 1, 2, 3, 4, 5, 6, 7]}

parcours = {0: [1, 2, 3, 4, 5, 7, 10],
1: [4],
2: [2, 5, 6, 7, 8, 9],
3: [0, 9, 10],
4: [1, 2, 5, 7, 10],
5: [0, 1, 3, 4, 6, 8, 9],
6: [0, 1, 3, 4, 6, 8, 9, 10],
7: [0, 1, 2, 3, 4, 5, 6, 7, 8],
8: [0, 2, 3, 5, 6, 7, 8, 9, 10]}


# Pour indiquer où poser des 1 dans la matrice creuse 'matrix'
rows = [key for key in parcours.keys() for _ in range(len(parcours[key]))]
cols = [stud for studs in parcours.values() for stud in studs]


# Matrice creuse définie de manière suivante : lignes = parcours (p), colonnes = étudiants (e)
# matrix[p, e] = 1 si la paire (p, e) est possible, = 0 sinon
matrix = csr_array(([1] * len(rows), (rows, cols)), shape=(nparcours, netudiants), dtype=int)

m = gp.Model("Ex3")

# Ajouter uniquement les contraintes nécessaires
x = m.addVars(((p, s) for p in range(nparcours)
              for s in range(netudiants) if matrix[p, s] > 0), vtype=GRB.BINARY, name="x")

valid_parcours = {p for p, _ in x.keys()}
valid_etudiants = {e for _, e in x.keys()}

# Contraintes sur les capacités des parcours
m.addConstrs((gp.quicksum(x[i, j] for j in parcours[i]) <= caps[i] for i in parcours.keys() if parcours[i]))

# Contraintes que chaque étudiant doit être affecté à au plus 1 parcours
m.addConstrs((gp.quicksum(x[p, j] for p in [p for (p, e) in x.keys() if e == j]) <= 1 for j in valid_etudiants))

# Fonction objective : maximiser le nombre des étudiants affectés aux parcours
m.setObjective(gp.quicksum(x[i, j] for (i, j) in x.keys()), GRB.MAXIMIZE)

m.optimize()
m.write("solution_k4.lp")
print(m.status)

for v in m.getVars():
    if v.X > 0:
        print(f"{v.VarName}={v.X}")
