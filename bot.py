from constructors import c, d, b
from simulator import sim




class Bot:
    def __init__(self, sim,style, preset, balance = 1000):
        self.name = b.set_bot_name(self)
        self.sim = sim
        self.style = style
        self.prset = preset


bao = Bot(sim, 'Bolbot', 'hardcore')
print(bao.name)
print(bao.sim.raw_df)