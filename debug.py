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

for n in range(5000):
    print(n)
    tst.sim.update_df(n)
    # print(tst.sim.df)
    tst.run_main()
    print(tst.trade_history)
    print(tst.orders)
