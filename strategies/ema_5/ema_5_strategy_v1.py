
from colorama import Fore
import pandas as pd
import datetime
import time
import talib
import threading
import logging
from utilities import algo_util as utility


def process(name):
    risk_capacity = 100
    ema_period = 5
    timeframe = '5min'
    tgt_multiplier = 2
    traded = False

    while getTradeTime() and traded is False:
        try:
            dx = utility.get_historical_data(name="NSE:" + name + "-EQ", interval=timeframe, timeperiod=3)
            df = pd.DataFrame()
            df = df.append(dx)

            df['5ema'] = talib.EMA(df['close'], timeperiod=ema_period)

            signal_candle = df.iloc[-2]
            current_candle = df.iloc[-1]

            signal_candle_formed = signal_candle['low'] > signal_candle['5ema']
            sell_signal_formed = current_candle['low'] < signal_candle['low']

            logging.warning(f"Signal for trade : {signal_candle_formed and sell_signal_formed and traded is False} for {name}")
            if signal_candle_formed and sell_signal_formed and traded is False:
                print(f"{Fore.YELLOW} Signal for {name} on {datetime.datetime.now().time()} {Fore.WHITE} \n")
                sl = signal_candle['high'] + 0.10

                try:
                    qty = int(risk_capacity / (sl - signal_candle['low']))
                except Exception as e:
                    print(f"trade not taken for {name} as SL, entry values are not valid")
                    return

                if qty <= 0:
                    print(f"trade not taken for {name} as SL value exceeds risk capacity")
                else:
                    sl_points = round((sl - signal_candle['low']) * 20.0) / 20.0
                    tg_points = round((tgt_multiplier * sl_points) * 20.0) / 20.0

                    data = {
                        "symbol": "NSE:" + name + "-EQ",
                        "qty": qty,
                        "type": 2,
                        "side": -1,
                        "productType": "BO",
                        "limitPrice": 0,
                        "stopPrice": 0,
                        "validity": "DAY",
                        "disclosedQty": 0,
                        "offlineOrder": "False",
                        "stopLoss": sl_points,
                        "takeProfit": tg_points
                    }
                    response = utility.place_order(data)
                    print(f"Response : {response}")
                    if response is not None:
                        traded = True

        except Exception as e:
            print(f"Error occurred : {e}")
        time.sleep(3)

def getTradeTime():
    return datetime.time(9, 15) < datetime.datetime.now().time() < datetime.time(10, 00)

def ema5Strategy(watchlist):

    for name in watchlist:
        x = threading.Thread(target=process, args=(name,))
        print(f"Thread started for {name}")
        x.start()
        time.sleep(3)
def main():
    print("Scheduler started... ")
    utility.fyers_login()

    watchlist = [
        'POWERGRID'
        ,'MARUTI'
        ,'BRITANNIA'
        ,'IOC'
        ,'SBILIFE'
        ,'M&M'
        ,'SHREECEM'
        ,'EICHERMOT'
        ,'DRREDDY'
        ,'NTPC'
        ,'CIPLA'
        ,'SBIN'
        ,'LT'
        ,'ONGC'
        ,'UPL'
        ,'HEROMOTOCO'
        ,'DIVISLAB'
        ,'WIPRO'
        ,'RELIANCE'
        ,'ITC']
    ema5Strategy(watchlist)

if __name__ == '__main__':
    main()




