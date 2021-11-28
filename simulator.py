from constructors import c, d
from Io import io


class Simulator:

    """Simulates candle by candle with the update fucntion"""

    def __init__(self, call_name, min_rows):
        self.name = call_name
        self.ticker = "{}".format(c.break_call_name(self.name)["ticker"])
        self.tf = c.break_call_name(self.name)["tf"]
        self.raw_df = d.apply_indics(
            d.resize_df(d.load_df_from_raw_file(self.name), min_rows)
        )
        self.df = self.update_df(0)
        self.min_rows = min_rows
        io.print_bull("sim {} loaded".format(self.name))

    def update_df(self, row):
        self.df = self.raw_df.iloc[row]
        return self.df

    def get_last(self, var):
        return self.df[var]

sim = Simulator('BTCUSDT5m', 5000)
