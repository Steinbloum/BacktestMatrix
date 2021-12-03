from bot import Bot
from constructors import b
from Io import Io
import numpy as np

io = Io()


class Bolbot(Bot):
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
        # print(self.preset)
        # print(self.params)
        # input()
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
                "bias": "neutral",
                "order_type": "limit",
                "charting options": ["bolup", "boldown"],
            }
        }
        return params_dict


class Presetbot(Bot):
    """This is the preset for making new bots, copy this and fill what is needed"""

    def __init__(self, sim, style, preset, balance=1000):
        super().__init__(sim, style, preset, balance=balance)
        self.params = b.load_attributes("bot_config.json", self.style, self.preset)
        io.print_statement("{} is awake".format(self.name))

    def set_orders(self):

        """returns the order list or dict"""
        orders = {}
        if not self.position:
            """Set the opening orders"""
            open_long = {
                "price": "",
                "value": "",
                "size": "",
                "side": "buy",
                "motive": "open",
                "pos_side": "long",
            }
            open_short = {
                "price": "",
                "value": "",
                "size": "",
                "side": "buy",
                "motive": "open",
                "pos_side": "long",
            }
            return [open_long, open_short]

        if self.position:
            """set stop and tp here, for now only one TP is allowed, no partial TP"""
            df = self.trade_history.loc[
                self.trade_history["trade_count"] == self.trade_count
            ]

            initial_value = float(df["value"].loc[df["motive"] == "open"])
            initial_price = float(df["price"].loc[df["motive"] == "open"])

            ########
            """Set the stop here, by default it's stopping when the value is inferior to what is set in the params"""
            ########

            if self.position["side"] == "long":
                stop_value = initial_value * self.params["trigger_sl"]
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
                side = "sell"
            elif self.position["side"] == "short":
                stop_value = initial_value * (1 - self.params["trigger_sl"] + 1)
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
                side = "buy"
            stop = {
                "price": stop_price,
                "value": stop_value,
                "size": self.position["size"],
                "side": side,
                "motive": "stop",
            }
            ########
            """Set the tp here"""
            ########

            if self.position["side"] == "long":
                tp_price = "SET THE TP PRICE FOR LONG"
            if self.position["side"] == "short":
                tp_price = "SET THE TP PRICE FOR SHORT"
            tp_value = float(df["size"].loc[df["motive"] == "open"]) * tp_price
            size = -self.position["size"]
            tp = {
                "price": tp_price,
                "value": tp_value,
                "size": size,
                "side": side,
                "motive": "tp",
            }
            return {"stop": stop, "tp": tp}

    def run_main(self):
        "runs the bot, only touch the condition"
        b.update_position_value(self)
        if self.sim.df[
            "INDICATOR"
        ]:  # Replace 'INDICATOR' by the indicator to start the analysis
            self.orders = self.set_orders()
            self.run_bot()

    def get_params_dict(self):
        """Set your parametrers dict for config"""
        params_dict = {
            self.style: {
                "preset": "standard",  # you need to change the preset here before calling the create config function below
                "trade amount": 0.5,
                "trigger_sl": 0.9,
                "bias": "neutral",
                "order_type": "limit",
                "charting options": [
                    ""
                ],  # experimental for now, set here a list of indicators to show on the sibngle trade chart
            }
        }
        return params_dict


class Emabot(Bot):
    def __init__(self, sim, style, preset, balance=1000):
        super().__init__(sim, style, preset, balance=balance)
        self.params = b.load_attributes("bot_config.json", self.style, self.preset)
        io.print_statement("{} is awake".format(self.name))
        self.trend = None
        self.trend_count = 0

    def set_orders(self):

        """returns the order list or dict"""
        open_orders = []
        if not self.position:
            """Set the opening orders"""
            ls = []
            for ema in self.params["emas"]:
                ls.append(self.sim.df[ema])

            if ls == list(np.sort(ls)[::-1]):
                trend = "bull"
                if trend == self.trend:
                    self.trend_count += 1
                else:
                    self.trend = trend
                    self.trend_count = 0
            elif ls == list(np.sort(ls)):
                trend = "bear"
                if trend == self.trend:
                    self.trend_count += 1
                else:
                    self.trend = trend
                    self.trend_count = 0

            if (
                self.trend == "bull"
                and self.trend_count >= self.params["trend_validation_period"]
            ):
                price = self.sim.df[
                    self.params["emas"][int(self.params["opening_order"])]
                ]
                value = self.balance * self.params["trade_amount"]
                size = value / price
                open_long = {
                    "price": price,
                    "value": value,
                    "size": size,
                    "side": "buy",
                    "motive": "open",
                    "pos_side": "long",
                }
                open_orders.append(open_long)

            elif (
                self.trend == "bear"
                and self.trend_count >= self.params["trend_validation_period"]
            ):
                price = self.sim.df[
                    self.params["emas"][int(self.params["opening_order"])]
                ]
                value = self.balance * self.params["trade_amount"]
                size = value / price
                open_short = {
                    "price": price,
                    "value": value,
                    "size": size,
                    "side": "sell",
                    "motive": "open",
                    "pos_side": "short",
                }
                open_orders.append(open_short)

            return open_orders

        if self.position:
            """set stop and tp here, for now only one TP is allowed, no partial TP"""
            df = self.trade_history.loc[
                self.trade_history["trade_count"] == self.trade_count
            ]

            initial_value = float(df["value"].loc[df["motive"] == "open"])
            initial_price = float(df["price"].loc[df["motive"] == "open"])

            ########
            """Set the stop here, by default it's stopping when the value is inferior to what is set in the params"""
            ########

            if self.position["side"] == "long":
                stop_value = initial_value * self.params["trigger_sl"]
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
                side = "sell"
            elif self.position["side"] == "short":
                stop_value = initial_value * (1 - self.params["trigger_sl"] + 1)
                stop_price = stop_value / float(df["size"].loc[df["motive"] == "open"])
                side = "buy"
            stop = {
                "price": stop_price,
                "value": stop_value,
                "size": self.position["size"],
                "side": side,
                "motive": "stop",
            }
            ########
            """Set the tp here"""
            ########

            if self.position["side"] == "long":
                delta = (
                    self.sim.df[self.params["emas"][int(self.params["tp_delta"][0])]]
                    - self.sim.df[self.params["emas"][int(self.params["tp_delta"][1])]]
                ) * self.params["tp_multiplicator"]
                tp_price = self.sim.df[self.params["emas"][0]] + delta
            if self.position["side"] == "short":
                delta = (
                    self.sim.df[self.params["emas"][1]]
                    - self.sim.df[self.params["emas"][0]]
                ) * 2
                tp_price = self.sim.df[self.params["emas"][0]] - delta
            tp_value = float(df["size"].loc[df["motive"] == "open"]) * tp_price
            size = -self.position["size"]
            tp = {
                "price": tp_price,
                "value": tp_value,
                "size": size,
                "side": side,
                "motive": "tp",
            }
            # print("tp is {}, stop is {}".format(tp_price, stop_price))
            # input()
            return {"stop": stop, "tp": tp}

    def run_main(self):
        "runs the bot, only touch the condition"
        # print(self.preset)
        # print(self.params)
        # input()
        b.update_position_value(self)
        if self.sim.df[self.params["emas"][-1]]:
            self.orders = self.set_orders()
            self.run_bot()

    def get_params_dict(self):
        """Set your parametrers dict for config"""
        params_dict = {
            self.style: {
                "preset": "std",  # you need to change the preset here before calling the create config function below
                "trade_amount": 0.5,
                "trigger_sl": 0.9,
                "bias": "neutral",
                "emas": ["EMA10", "EMA25", "EMA50"],
                "trend_validation_period": 5,
                "opening_order": 0,  # the buy or sell will be set on the index of the emalist above
                "tp_delta": [
                    0,
                    1,
                ],  # the two emas of the ema list on wich the delta is calculated
                "tp_multiplicator": 2,  # the mulitplicator of the delta for the tp
                "order_type": "limit",
                "charting options": [
                    "EMA10",
                    "EMA25",
                    "EMA50",
                ],  # experimental for now, set here a list of indicators to show on the sibngle trade chart
            }
        }
        return params_dict


# from simulator import Simulator

# sim = Simulator("ETHUSDT1m", 5)
# ####
# """below is the function call to make a new config"""
# ####

# b.create_config("bot_config.json", Emabot(sim, "Emabot", "standard"))
