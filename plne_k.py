import gurobipy as gp
from gurobipy import GRB
import numpy as np
from scipy.sparse import csr_array

m = gp.Model("Ex3")

nparcours, netudiants = 9, 11  # rows = parcours, column = etudiants

parcours = np.arange(0, 10, 1, int)
etudiants = np.arange(0, 11, 1, int)
caps = [2, 1, 1, 1, 1, 1, 1, 1, 2]

data = [1] * 12
rows = [0, 0, 2, 4, 5, 5, 5, 6, 6, 6, 7, 7]
cols = [5, 7, 9, 10, 0, 1, 3, 0, 1, 3, 6, 7]

matrix = csr_array((data, (rows, cols)), shape=(nparcours, netudiants), dtype=int)
x = m.addVars(nparcours, netudiants, vtype=GRB.BINARY, name="x")

# Constraints on capacity
m.addConstrs((gp.quicksum(x[i, j]
              for j in range(netudiants) if matrix[i, j] > 0) <= caps[i] for i in range(nparcours) if (matrix[i].toarray() > 0).any()))

# Constraints on max 1 master
m.addConstrs((gp.quicksum(x[i, j] for i in range(nparcours)) <= 1 for j in range(netudiants)
              if (matrix._getcol(j).toarray() > 0).any()))

m.setObjective(gp.quicksum(x[i, j] * matrix[i, j] for i in range(nparcours)
               for j in range(netudiants)), GRB.MAXIMIZE)

for i in range(nparcours):
    print(i, (matrix[i].toarray() > 0).any())

m.optimize()
m.write("solution_k4.lp")
print(m.status)
for v in m.getVars():
    if v.X > 0:
        print(f"{v.VarName}={v.X}")
# m.addConstr()
