from os import path
from constructors import b


class Bot:
    def __init__(self, sim, style, preset, balance=1000):
        self.name = b.set_bot_name(self)
        self.sim = sim
        self.style = style
        self.preset = preset
        self.balance = balance
        self.trade_history = b.init_history(self)
        self.orders = False
        self.trade_count = 0
        self.position = False

    def run_bot(self):
        if not self.position:
            if self.orders:
                if type(self.orders) == list:
                    for order in self.orders:
                        if self.sim.df["low"] < order["price"] < self.sim.df["high"]:
                            b.open_position(self, order["pos_side"])
                            b.store_transaction(self, b.execute_order(self, order))
                            self.set_orders()
                            break

        if type(self.orders) is dict:
            if self.sim.df["low"] < self.orders["stop"]["price"] < self.sim.df["high"]:
                b.store_transaction(self, b.execute_order(self, self.orders["stop"]))
                b.close_position(self)

            elif self.sim.df["low"] < self.orders["tp"]["price"] < self.sim.df["high"]:
                b.store_transaction(self, b.execute_order(self, self.orders["tp"]))
                b.close_position(self)
