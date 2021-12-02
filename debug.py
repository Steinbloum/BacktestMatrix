from subbots import Testbot
from matrix import Matrix

# rows = 2000
# sim = Simulator(s.get_random_sim_list(1, rows)[0], rows)
# tst = Testbot(sim, "testbot", "standard")


# for n in range(rows):
#     # print(n)
#     if n % 100 == 0:
#         print("analysing candle {}".format(n))
#     tst.sim.update_df(n)
#     tst.run_main()
# print(tst.trade_history)
# tst.trade_history.to_csv("tests/test_trade_hist.csv")
# p.perf_chart(tst)
# p.make_chart_report(tst.trade_history, tst.sim.raw_df, path="tests")

botlist = [[Testbot, "testbot", "standard"]]
matrix = Matrix()
matrix.run_sim(2, botlist, 2000)

print(matrix.name)
