from subbots import Bolbot, Emabot
from matrix import Matrix


botlist = [[Emabot, "Emabot", "std"], [Bolbot, "Bolbot", "standard"]]
matrix = Matrix()
matrix.run_sim(10, botlist, 20000)

print(matrix.name)
