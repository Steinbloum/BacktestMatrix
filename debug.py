from constructors import c, d, b
from simulator import Simulator
from subbots import Testbot


sim = Simulator("BTCUSDT5m", 5000)
tst = Testbot(sim, "testbot", "standard")
# # print(bao.name)
# # print(bao.sim.raw_df)
# # b.store_transaction(bao, None)
# # print(bao.trade_history)
# bao.params = {"order_type": "limit"}
# order = {
#     "price": 100,
#     "value": 100,
#     "size": 1,
#     "side": "buy",
#     "motive": "open",
# }
# b.open_position(bao, "long")
# b.store_transaction(bao, b.execute_order(bao, order))
# print(bao.trade_history)
# print(bao.balance)
# print(bao.position)
# input()
# order = {
#     "price": 200,
#     "value": 200,
#     "size": 1,
#     "side": "sell",
#     "motive": "tp",
# }
# b.store_transaction(bao, b.execute_order(bao, order))
# print(bao.trade_history)
# print(bao.balance)
# print(bao.position)
# b.close_position(bao)
# print(bao.position)
# print(bao.balance)
# input()
# order = {
#     "price": 250,
#     "value": 250,
#     "size": 1,
#     "side": "sell",
#     "motive": "open",
# }
# b.open_position(bao, "short")
# b.store_transaction(bao, b.execute_order(bao, order))

# print(bao.trade_history)
# print(bao.balance)
# print(bao.position)
# input()
# order = {
#     "price": 200,
#     "value": 200,
#     "size": 1,
#     "side": "buy",
#     "motive": "tp",
# }
# b.store_transaction(bao, b.execute_order(bao, order))
# print(bao.trade_history)
# print(bao.balance)
# print(bao.position)
# b.close_position(bao)
# print(bao.position)
# print(bao.balance)
# print(bao.trade_history)


for n in range(2000):
    tst.sim.update_df(n)
    print(n)
    tst.run_main()
    print("H{} L{}".format(tst.sim.df["high"], tst.sim.df["low"]))
    print("pos is {}".format(tst.position))

    if not tst.position:
        if tst.orders:
            for order in tst.orders:
                if tst.sim.df["low"] < order["price"] < tst.sim.df["high"]:
                    # print("###########################IM IN RANGE")
                    # print(order)
                    b.open_position(tst, order["pos_side"])
                    b.store_transaction(tst, b.execute_order(tst, order))
                    # print(tst.position)
                    # print(tst.trade_history)
                    # input()
    elif tst.position:
        if tst.sim.df["low"] < tst.orders["stop"]["price"] < tst.sim.df["high"]:
            # print("pos val is {}".format(tst.position["value"]))

            b.store_transaction(tst, b.execute_order(tst, tst.orders["stop"]))
            b.close_position(tst)

            # print("i stoped")
            # print(tst.trade_history)
            # print(tst.position)

        elif tst.sim.df["low"] < tst.orders["tp"]["price"] < tst.sim.df["high"]:
            # print("pos val is {}".format(tst.position["value"]))
            b.store_transaction(tst, b.execute_order(tst, tst.orders["tp"]))
            # print("balance is {}".format(tst.balance))
            # print(tst.position)
            # print("i tped")
            b.close_position(tst)
            # input()
print(tst.trade_history)
tst.trade_history.to_csv("tests/test_trade_hist.csv")
