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
        if self.orders:
            if not self.position:
                if (
                    self.sim.df["low"]
                    < self.orders["open"]["price"]
                    < self.sim.df["high"]
                ):
                    if self.orders["open"]["side"] == "buy":
                        side = "long"
                    else:
                        side = "short"
                    b.open_position(self, side)
                    b.store_transaction(
                        self, b.execute_order(self, self.orders["open"])
                    )
                    print(self.position)
                    print(self.trade_history)
                    input()
            else:
                if (
                    self.sim.df["low"]
                    < self.orders["stop"]["price"]
                    < self.sim.df["high"]
                ):
                    b.store_transaction(
                        self, b.execute_order(self, self.orders["stop"])
                    )
                    print("i stoped")
                    print(self.trade_history)
                    print(self.position)
                    input()
                if (
                    self.sim.df["low"]
                    < self.orders["tp"]["price"]
                    < self.sim.df["high"]
                ):
                    b.store_transaction(self, b.execute_order(self, self.orders["tp"]))
                    print("i tped")
                    print(self.trade_history)
                    print(self.position)
                    input()
        else:
            print("just chillin")
