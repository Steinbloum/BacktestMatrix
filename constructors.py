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
from datetime import datetime

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
                rand = random.randrange(size, len(df))
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
                pnl = value - df["value"].iloc[0]
            else:
                pnl = df["value"].iloc[0] - value
        if order["motive"] == "tp" or order["motive"] == "stop":
            balance = bot.balance
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
        # print(bot.position)

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


class Plotter:
    def __init__(self) -> None:
        pass

    def perf_chart(
        self, trade_hist, raw, max_klines, bot_name, asset, initial_wallet, path
    ):
        """make a line chart asset perf vs bot perf"""
        td = trade_hist[trade_hist["motive"].isin(["tp", "stop", "close"])]
        raw = raw[["Date", "close"]]
        raw = raw.iloc[-max_klines:]
        # print("making report for {}".format(bot_name))
        asset_start_price = raw["close"].iloc[0]
        asset_end_price = raw["close"].iloc[-1]
        asset_roi = round(asset_end_price / asset_start_price * 100 - 100, 2)
        bot_roi = round(td["balance"].iloc[-1] / initial_wallet * 100 - 100, 2)
        if bot_roi >= asset_roi:
            msg = "Good bot beat the market !"
        else:
            msg = "Bad bot did not outperform the market"
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=raw["Date"], y=raw["close"], name=asset))
        fig.add_trace(
            go.Scatter(x=td["Date"], y=td["balance"], name=bot_name),
            secondary_y=True,
        )
        fig.update_layout(
            title="Asset ROI : {}% bot ROI : {}%\n" "{}".format(asset_roi, bot_roi, msg)
        )
        fig.update_yaxes(title_text="<b>Asset price</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Bot balance</b>", secondary_y=True)
        fig.write_image("tests/perfo.png")

    def get_chart_graph(
        self, df, start_index, end_index, trade_history, path, name, trade_count
    ):

        df = df.loc[start_index:end_index]

        trade_history = trade_history.loc[trade_history["trade_count"] == trade_count]
        buy = trade_history.loc[trade_history["side"] == "buy"]
        sell = trade_history.loc[trade_history["side"] == "sell"]

        # print(trade_history)
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["Date"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                )
            ]
        )
        side = trade_history["position side"].iloc[0].upper()
        value = round(trade_history["value"].iloc[0], 2)
        pnl = round(sum(trade_history["pnl"].dropna()), 2)
        roi = round(
            sum(trade_history["pnl"].dropna()) / trade_history["value"].iloc[0] * 100, 2
        )
        if side == "SHORT":
            value *= -1
            roi *= -1
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            showlegend=False,
            title="{} - Value : {}$, PNL : {}, ROI : {}%".format(side, value, pnl, roi),
        )

        fig.add_trace(
            go.Scatter(
                x=sell["Date"],
                y=sell["price"],
                mode="markers",
                marker=dict(
                    color="red", size=15, line=dict(width=2, color="DarkSlateGrey")
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=buy["Date"],
                y=buy["price"],
                mode="markers",
                marker=dict(
                    color="green", size=15, line=dict(width=2, color="DarkSlateGrey")
                ),
            )
        )
        trade_history = None
        fig.write_image("{}/{}.png".format(path, name))
        print("writing to{}/{}.png".format(path, name))
        return fig

    def make_chart_report(self, trade_history, raw_df, path):
        """Get the top 10 best trades and worst 10 to graph"""
        top = trade_history["pnl"].sort_values(ascending=False).head(10).index.tolist()
        worst = (
            trade_history["pnl"].sort_values(ascending=False).tail(10).index.tolist()
        )
        toppairs = []
        worstpairs = []
        for n in range(len(top)):

            toppairs.append([top[n] - 1, top[n]])
            worstpairs.append([worst[n] - 1, worst[n]])
        n = 1
        for indexes in toppairs:
            idx = self.get_index_range(
                raw_df,
                trade_history["Date"].iloc[indexes[0]],
                trade_history["Date"].iloc[indexes[1]],
            )
            # print(idx)
            trade_count = trade_history["trade_count"].iloc[indexes[0]]
            # print("tradect {}".format(trade_count))
            self.get_chart_graph(
                raw_df,
                idx["start"],
                idx["end"],
                trade_history,
                trade_count=trade_count,
                path=path,
                name="top{}".format(n),
            )
            fig = None
            n += 1
        n = 1
        worstpairs = reversed(worstpairs)
        for indexes in worstpairs:
            idx = self.get_index_range(
                raw_df,
                trade_history["Date"].iloc[indexes[0]],
                trade_history["Date"].iloc[indexes[1]],
            )
            # print(idx)
            trade_count = trade_history["trade_count"].iloc[indexes[0]]
            # print("tradect {}".format(trade_count))
            self.get_chart_graph(
                raw_df,
                idx["start"],
                idx["end"],
                trade_history,
                trade_count=trade_count,
                path=path,
                name="worst{}".format(n),
            )
            fig = None
            n += 1

    def get_index_range(self, raw_df, start, end, delta=75):
        """get the index of the delta candles in the raw DF for the plotting
        Date is str format"""
        # start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        # end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        df = raw_df
        stdt = df.index[df["Date"] == start].to_list()
        # print(stdt)
        stdt = stdt[0] - delta
        endt = df.index[df["Date"] == end].to_list()
        endt = endt[0] + delta

        return {"start": stdt, "end": endt}


class Sim_manager:
    def __init__(self) -> None:
        pass

    def get_random_sim_list(self, amount, max_klines, conditions=True):
        ls = []
        while len(ls) < amount:
            for n in range(amount):
                lssimis = random.choice(os.listdir(path_to_data))
                tfs = random.choice(["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
                pair = lssimis + tfs
                if not pair in ls:
                    if conditions:
                        if self.check_for_data(pair, max_klines):
                            ls.append(pair)
                        else:
                            io.print_warning("NO DATA FOR {}".format(pair))
        print(ls)
        return ls

    def check_for_data(self, call_name, max_klines):
        call = self.get_ticker_tf(call_name)
        ticker = "{}{}".format(call["coin"], call["pair"])
        tf = call["tf"]
        path_to_file = "{}/{}/{}/{}_{}.csv".format(path_to_data, ticker, tf, ticker, tf)
        if os.path.isfile(path_to_file):
            # print("Data on {} found".format(call_name))
            df = pd.read_csv(path_to_file)
            if len(df) > max_klines:
                return True
        else:
            print("NO SUFFICIENT DATA FOR {}!".format(call_name))
            return False

    def get_ticker_tf(self, string):
        pairs = ["USDT", "EUR"]
        tfs = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "12h", "1d", "3d", "1w"]
        for pair in pairs:
            if string.find(pair) != -1:
                string = string.replace(pair, "")
                break
        for tf in tfs:
            if string.find(tf) != -1:
                string = string.replace(tf, "")
                break
        coin = string
        return {"coin": coin, "pair": pair, "tf": tf}


c = Constructor()
d = Dataframe_manager()
b = Bot_manager()
p = Plotter()
s = Sim_manager()
