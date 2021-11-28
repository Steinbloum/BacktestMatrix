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

class Dataframe_manager:
    '''Everything that is relative to dataframe operations'''
    def __init__(self):
        pass

    def load_df_from_raw_file(self, call_name):
        """returns de dataframe for the selected pair, returns false if no path"""
        path_to_raw_file = c.get_path_to_raw_file(call_name)
        if path_to_raw_file:
            df = pd.read_csv(path_to_raw_file, index_col=0)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        else:
            return False

    def resize_df(self, df, size, random_start = True):
        '''resizes the DF to the size and returns a DF with a random start if True'''
        if len(df) < size:
            return False
        else:
            if not random_start:
                df = df.iloc[-size:]
                return df
            if random:
                rand = random.randrange(3000,len(df))
                df = df.iloc[-rand:-rand+size]
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
    '''everything relative to the bot management'''
    pass
    def __init__(self):
        pass
    
    def set_bot_name(self, bot):
        bot.name = "{}_the_{}".format(
            names.get_first_name(gender="female"),
            r.word(include_parts_of_speech=["adjectives"]),
        )
        return bot.name

c = Constructor()
d = Dataframe_manager()
b = Bot_manager()

