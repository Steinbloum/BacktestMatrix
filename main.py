from subbots import Bolbot
from matrix import Matrix


botlist = [[Bolbot, "Bolbot", "standard"]]
matrix = Matrix()
matrix.run_sim(20, botlist, 50000)
