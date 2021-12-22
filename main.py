from subbots import Bolbot, Emabot
from matrix import Matrix


botlist = [[Bolbot, "Bolbot", "standard"]]
matrix = Matrix()
matrix.run_sim(10, botlist, 5000)

print(matrix.name)
