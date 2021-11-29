from re import escape
from ta.volume import money_flow_index
from ta.trend import ema_indicator, macd, EMAIndicator, macd_signal
from ta.volatility import (
    bollinger_mavg,
    bollinger_hband,
    bollinger_lband,
    bollinger_lband_indicator,
    bollinger_hband_indicator,
)
import os
import pandas as pd
import names
from wonderwords import RandomWord
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
from Io import io

r = RandomWord()

path_to_data = os.getenv("PATHTODATA")


class Constructor:
    """A class for everything relative to construction"""

    def __init__(self):
        pass

    def break_call_name(self, call_name):
        """Returns a dict for the call_name of the simulation
        ex: 'ETHUSDT15m returns
        {"pair": USDT, "tf": 15m, "coin": ETH, "ticker": ETHUSDT}
        """
        pairs = ["USDT", "EUR"]
        tfs = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "12h", "1d", "3d", "1w"]
        for pair in pairs:
            if pair in call_name:
                call_name = call_name.replace(pair, "")
                break
            else:
                print("PAIR ERROR")
        for tf in tfs:
            if tf in call_name:
                if tf == "5m":
                    if call_name[call_name.find(tf) - 1] != "1":
                        call_name = call_name.replace(tf, "")
                        break
                else:
                    call_name = call_name.replace(tf, "")
                    break

        coin = call_name
        return {"pair": pair, "tf": tf, "coin": coin, "ticker": coin + pair}

    def create_dir(self, dirpath):
        path = dirpath
        if not os.path.isdir(path):
            os.makedirs(path)
            return path
        else:
            return path

    def get_path_to_raw_file(self, call_name):
        """returns the path to the raw data or False"""
        call = self.break_call_name(call_name)
        ticker = call["ticker"]
        tf = call["tf"]
        path = "{}/{}/{}/{}.csv".format(
            path_to_data, ticker, tf, "{}_{}".format(ticker, tf)
        )
        if os.path.isfile(path):
            return path
        else:
            # print("NO DATA")
            return False

    def add_to_json(self, json_file, new_config, bot_type):
        ls = []
        with open(json_file, "r") as file:
            if os.stat(json_file).st_size == 0:
                ls.append(new_config)
                print("appending config")
                with open(json_file, "w") as file:
                    json.dump(json.dumps(ls), file)
                    print("config stored")
                    return new_config
            else:
                stock = json.load(file)
                ls = json.loads(stock)
                for item in ls:
                    print(item)
                    try:
                        item[bot_type]["preset"] == new_config[bot_type]["preset"]
                    except KeyError:
                        ls.append(new_config)
                        print("appending config")
                        with open(json_file, "w") as file:
                            json.dump(json.dumps(ls), file)
                            print("config stored")
                            break
                    if item[bot_type]["preset"] == new_config[bot_type]["preset"]:
                        print("preset already stored")
                    else:
                        ls.append(new_config)
                        print("appending config")
                        with open(json_file, "w") as file:
                            json.dump(json.dumps(ls), file)
                            print("config stored")
                            break


class Dataframe_manager:
    """Everything that is relative to dataframe operations"""

    def __init__(self):
        pass

    def load_df_from_raw_file(self, call_name):
        """returns de dataframe for the selected pair, returns false if no path"""
        path_to_raw_file = c.get_path_to_raw_file(call_name)
        if path_to_raw_file:
            df = pd.read_csv(path_to_raw_file, index_col=0)
            df["Date"] = pd.to_datetime(df["Date"])
            return df
        else:
            return False

    def resize_df(self, df, size, random_start=True):
        """resizes the DF to the size and returns a DF with a random start if True"""
        if len(df) < size:
            return False
        else:
            if not random_start:
                df = df.iloc[-size:]
                return df
            if random:
                rand = random.randrange(3000, len(df))
                df = df.iloc[-rand : -rand + size]
                return df

    def apply_indics(self, df):
        """Applies indicators to the df
        WARNING : make sure to apply to a resized DF els it might take forever"""

        df["mfi"] = money_flow_index(df.high, df.low, df.close, df.volume)
        df["macd"] = macd(df.close)
        df["macds"] = macd_signal(df.close)
        df["bolup"] = bollinger_hband(df.close)
        df["bolupcross"] = bollinger_hband_indicator(df.close)
        df["bolmav"] = bollinger_mavg(df.close)
        df["boldown"] = bollinger_lband(df.close)
        df["boldowncross"] = bollinger_lband_indicator(df.close)
        df["EMA10"] = ema_indicator(df.close, window=10)
        df["EMA25"] = ema_indicator(df.close, window=25)
        df["EMA50"] = ema_indicator(df.close, window=50)
        df["EMA100"] = ema_indicator(df.close, window=100)
        df["EMA200"] = ema_indicator(df.close, window=200)
        return df


class Bot_manager:
    """everything relative to the bot management"""

    pass

    def __init__(self):
        pass

    def set_bot_name(self, bot):
        bot.name = "{}_the_{}".format(
            names.get_first_name(gender="female"),
            r.word(include_parts_of_speech=["adjectives"]),
        )
        return bot.name

    def init_history(self, bot):
        """Initalises the trade history Dataframe"""
        df = pd.DataFrame(
            {
                "Date": bot.sim.get_last("Date"),
                "price": bot.sim.get_last("close"),
                "size": None,
                "value": None,
                "side": None,
                "motive": "INIT",
                "pnl": None,
                "fees": None,
                "balance": bot.balance,
                "trade_count": 0,
                "position side": None,
            },
            index=[0],
        )
        return df

    def execute_order(self, bot, order):
        """Appends position to dict, makes operations on the balance and
        stores in the trade history"""
        fees = self.get_fees(order["value"], bot.params["order_type"])

        if order["side"] == "buy":
            bot.balance -= fees
            bot.balance -= order["value"]
            bot.position["value"] -= order["value"]
            bot.position["size"] += order["size"]
            bot.position["fees"] = fees

            return {
                "value": order["value"],
                "size": order["size"],
                "fees": fees,
                "price": order["price"],
                "motive": order["motive"],
                "side": order["side"],
            }
        else:
            bot.balance -= fees
            bot.balance += order["value"]
            bot.position["value"] += order["value"]
            bot.position["size"] -= order["size"]
            bot.position["fees"] = fees
            return {
                "value": order["value"],
                "size": order["size"],
                "fees": fees,
                "price": order["price"],
                "motive": order["motive"],
                "side": order["side"],
            }

    def store_transaction(self, bot, order):

        date = bot.sim.df["Date"]
        price = order["price"]
        if order["size"] < 0:
            size = -order["size"]
        else:
            size = order["size"]

        if order["value"] < 0:
            value = -order["value"]
        else:
            value = order["value"]
        side = order["side"]
        motive = order["motive"]

        if bot.position["size"] > 0:
            balance = bot.balance + order["value"]
        elif bot.position["size"] < 0:
            balance = bot.balance - order["value"]
        else:
            balance = bot.balance
        trade_count = bot.trade_count
        position_side = bot.position["side"]
        fees = order["fees"]
        if motive == "open":
            # print("motive is open, no pnl")
            pnl = None
        else:
            df = bot.trade_history.loc[
                bot.trade_history["trade_count"] == bot.trade_count
            ]
            # print(df)
            if bot.position["side"] == "long":
                pnl = order["value"] - df["value"].iloc[0]
            else:
                pnl = df["value"].iloc[0] - order["value"]
        ls = [
            date,
            price,
            size,
            value,
            side,
            motive,
            pnl,
            fees,
            balance,
            trade_count,
            position_side,
        ]
        bot.trade_history.loc[len(bot.trade_history)] = ls
        if bot.position["size"] == 0:
            self.close_position(self)

    def get_fees(self, amount, order_type):
        if order_type == "market":
            fees = amount * 0.0004
        else:
            fees = amount * 0.0002
        if fees < 0:
            fees *= -1
        return fees

    def open_position(self, bot, side):
        """initialiases the dict for bot.position, adds 1 to the trade count"""
        bot.trade_count += 1
        bot.position = {
            "trade count": bot.trade_count,
            "side": side,
            "value": 0,
            "size": 0,
        }
        print(bot.position)
        input("I entered")

    def close_position(self, bot):
        bot.position = False
        bot.orders = False

    def load_attributes(self, config_file, style, preset):
        with open(config_file, "r") as jsonfile:
            configs = json.load(jsonfile)
            configs = json.loads(configs)
            for item in configs:
                # print(item)
                for key, value in item.items():
                    if style == key:
                        if value["preset"] == preset:
                            print("FOUND PRESET")
                            return value
                        else:
                            print("WARNING NO CONFIG FOUND")
                            return False

    def create_config(self, config_file, bot, save=True):
        """set the paramters, return a dict to append to json"""
        """COMMENT THE INIT SECTION OF THE SUBBOT BEFORE RUNNING"""

        params = bot.get_params_dict()
        print(params)
        for key, value in params[bot.style].items():
            if key != "preset":
                if not value:
                    params[bot.style][key] = input(
                        "enter the param for {}\n".format(key)
                    )
        if save:
            c.add_to_json(config_file, params, bot.style)
        return params

    def update_position_value(self, bot):
        if bot.position:
            bot.position["value"] == bot.position["size"] * bot.sim.df["close"]


c = Constructor()
d = Dataframe_manager()
b = Bot_manager()
