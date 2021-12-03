# BacktestMatrix
this is the bakctest frame, the bots cannot go live for now


pip install reqs and 
DL Data from here : https://1drv.ms/u/s!Ak-BqSGEmNAli6dp26P6DnLA1FqOWQ?e=HfxdgU

make a .env file with the info below :

PUBLICAPI='YOUR PUBLIC KEY FOR BINANCE API' (not necessary if you don't want to DL moar data, in this case, leave blank)

PRIVATEAPI='YOUR PRIVATE KEY FOR BINANCE API' (not necessary if you don't want to DL moar data, in this case, leave blank)

PATHTODATA='THE PATH TOI THE DOWNLOADED DATA'


run main.py, it's already set up fot a session with 10 sims, 2 bots, and 20k candles. 
this setup is quite long, you can tweak the numbers as you wish. 

Once it's done go tchek the reports folder and enjoy data

To create a new bot : 

go to subbots.py, follow the template.

the availabale indicators are the ones in ta-lib, check their docs. you might need to add the indicator to the raw chart :
go to construstors.py => class Dataframe_manager => func add_indics() and add the new one

