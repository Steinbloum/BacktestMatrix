from simulator import Simulator
from subbots import Bolbot
from constructors import c, d, p, b, s, m
from Io import io


class Matrix:
    def __init__(self):
        pass
        self.sims = []
        self.bots = []
        self.name = None
        self.session_path = None
        self.session_results = None

    def init_sim(self, sim_amount, bot_list, candles_amount):
        sims = s.get_random_sim_list(sim_amount, candles_amount)
        for sim in sims:
            sim = Simulator(sim, candles_amount)
            self.sims.append(sim)
            for bot in bot_list:

                bot = bot[0](sim, bot[1], bot[2])
                c.create_dir("reports/{}/{}".format(self.name, bot.name))
                self.bots.append(bot)

    def run_sim(self, sim_amount, bot_list, candles_amount):
        m.init_session(self)
        self.init_sim(sim_amount, bot_list, candles_amount)
        for n in range(candles_amount):
            if n % 100 == 0:
                print("analysing candle {}".format(n))
            for sim in self.sims:
                sim.update_df(n)
            for bot in self.bots:
                bot.run_main()
        for bot in self.bots:
            b.close_all(bot, self.session_path)
            io.print_statement("Making reports for {}".format(bot.name))
            p.perf_chart(bot, self)
            p.make_chart_report(
                bot.trade_history,
                bot.sim.raw_df,
                "{}/{}/".format(self.session_path, bot.name),
                bot,
            )
        self.session_results = m.get_session_results(self, self.bots)
        io.print_statement("SESSION {} TERMINATED".format(self.name))
