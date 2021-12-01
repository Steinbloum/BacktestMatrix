from constructors import c, d, b, p, s
from simulator import Simulator
from subbots import Testbot

rows = 2000
sim = Simulator(s.get_random_sim_list(1, rows)[0], rows)
tst = Testbot(sim, "testbot", "standard")


for n in range(rows):
    print(n)
    if n % 100 == 0:
        print("analysing candle {}".format(n))
    tst.sim.update_df(n)
    tst.run_main()
print(tst.trade_history)
tst.trade_history.to_csv("tests/test_trade_hist.csv")
init_wallet = float(
    tst.trade_history["balance"].loc[tst.trade_history["motive"] == "INIT"]
)
print(init_wallet)
p.perf_chart(
    tst.trade_history,
    tst.sim.raw_df,
    tst.sim.min_rows,
    tst.name,
    tst.sim.ticker,
    init_wallet,
    "tests/",
)
p.make_chart_report(tst.trade_history, tst.sim.raw_df, path="tests")
