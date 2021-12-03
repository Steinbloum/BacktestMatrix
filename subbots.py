from bot import Bot
from constructors import b
from Io import Io

io = Io()


class Testbot(Bot):
    def __init__(self, sim, style, preset, balance=1000):
        super().__init__(sim, style, preset, balance=balance)
        self.params = b.load_attributes("bot_config.json", self.style, self.preset)
        io.print_statement("{} is awake".format(self.name))

    def set_orders(self):

        """returns the order list or dict"""
        orders = {}
        if not self.position:

            open_long = {
                "price": self.sim.df["boldown"],
                "value": self.balance * self.params["trade amount"],
                "size": self.balance
                * self.params["trade amount"]
                / self.sim.df["boldown"],
                "side": "buy",
                "motive": "open",
                "status": "open",
                "pos_side": "long",
            }
            open_short = {
                "price": self.sim.df["bolup"],
                "value": self.balance * self.params["trade amount"],
                "size": self.balance
                * self.params["trade amount"]
                / self.sim.df["bolup"],
                "side": "sell",
                "motive": "open",
                "pos_side": "short",
            }

            return [open_long, open_short]

        if self.position:
            df = self.trade_history.loc[
                self.trade_history["trade_count"] == self.trade_count
            ]

            initial_value = float(df["value"].loc[df["motive"] == "open"])
            initial_price = float(df["price"].loc[df["motive"] == "open"])

            if self.position["side"] == "long":
                stop_value = initial_value * self.params["trigger_sl"]
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
            elif self.position["side"] == "short":
                stop_value = initial_value * (1 - self.params["trigger_sl"] + 1)
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
            # print("stop value is {}, stop price is {}".format(stop_value, stop_price))
            # print(df)
            # print(
            #     "entry price is {}, stop price is {}".format(
            #         df["price"].loc[df["motive"] == "open"],
            #         stop_price,
            #     )
            # )
            # input()
            if self.position["side"] == "long":
                side = "sell"
            elif self.position["side"] == "short":
                side = "buy"
            stop = {
                "price": stop_price,
                "value": stop_value,
                "size": self.position["size"],
                "side": side,
                "motive": "stop",
            }
            # print("STOP is {}".format(stop))
            # input()

            if self.position["side"] == "long":
                tp_price = self.sim.df["bolup"]
                side = "sell"
            if self.position["side"] == "short":
                tp_price = self.sim.df["boldown"]
                side = "buy"
            tp_value = float(df["size"].loc[df["motive"] == "open"]) * tp_price
            size = -self.position["size"]

            tp = {
                "price": tp_price,
                "value": tp_value,
                "size": size,
                "side": side,
                "motive": "tp",
            }
            # print("TP is")
            # print(tp)

            return {"stop": stop, "tp": tp}

    def run_main(self):
        b.update_position_value(self)
        if self.sim.df["bolup"]:
            self.orders = self.set_orders()
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
                "charting options": ["bolup", "boldown"],
            }
        }
        return params_dict


# sim = Simulator("ETHUSDT1m", 5)

# b.create_config("bot_config.json", Testbot(sim, "testbot", "standard"))
