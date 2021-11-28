from constructors import c, d, b
from simulator import sim




class Bot:
    def __init__(self, sim,style, preset, balance = 1000):
        self.name = b.set_bot_name(self)
        self.sim = sim
        self.style = style
        self.preset = preset
        self.balance = balance
        self.trade_history = b.init_history(self)
        self.params = None #make the loading func
        

bao = Bot(sim, 'Bolbot', 'hardcore')
print(bao.name)
print(bao.sim.raw_df)
print(bao.trade_history)