from os import path
from constructors import c, d, b
from simulator import Simulator


class Bot:
    def __init__(self, sim, style, preset, balance=1000):
        self.name = b.set_bot_name(self)
        self.sim = sim
        self.style = style
        self.preset = preset
        self.balance = balance
        self.trade_history = b.init_history(self)
        self.orders = None
        self.trade_count = 0
        self.position = False

    def run_bot(self):

        print("just chillin")
