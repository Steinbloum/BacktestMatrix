from bot import Bot
from constructors import b


class Testbot(Bot):
    def __init__(self, sim, style, preset, balance=1000):
        super().__init__(sim, style, preset, balance=balance)
        self.params = b.load_attributes("bot_config.json", self.style, self.preset)

    def set_orders(self):

        open = {
            "price": self.sim.df["boldown"],
            "value": self.balance * self.params["trade amount"],
            "size": self.balance * self.params["trade amount"] / self.sim.df["boldown"],
            "side": "buy",
            "motive": "open",
            "status": "open",
        }
        value = open["value"]

        stop = {
            "price": self.sim.df["boldown"] * self.params["trigger_sl"],
            "value": value * self.params["trigger_sl"],
            "size": size,
            "side": "sell",
            "motive": "stop",
        }
        print("STOP SIZE IS {}".format(stop["size"]))
        input()
        tp = {
            "price": self.sim.df["bolup"],
            "value": self.sim.df["bolup"] / open["size"],
            "size": open["size"],
            "side": "sell",
            "motive": "tp",
        }
        print("{}, {}, {}".format(open, stop, tp))
        input()

        return {"open": open, "stop": stop, "tp": tp}

    def run_main(self):
        b.update_position_value(self)
        if self.sim.df["bolup"]:
            if not self.position:
                self.orders = self.set_orders()
                print(self.orders)
                self.run_bot()
            else:
                self.run_bot()

    def get_params_dict(self):
        params_dict = {
            self.style: {
                "preset": "standard",
                "trade amount": 0.5,
                "trigger_sl": 0.9,
                "ema": ["EMA25"],
                "bias": "neutral",
                "order_type": "limit",
                "charting options": ["EMA25"],
            }
        }
        return params_dict


# b.create_config("bot_config.json", Testbot(sim, "testbot", "standard"))
