
from colorama import Fore
import pandas as pd
import datetime
import time
import talib
import threading
from strategies.ema_5 import algo_util as utility

def process(name, traded):
    risk_capacity = 70
    ema_period = 5
    timeframe = '5min'
    tgt_multiplier = 3

    try:
        dx = utility.get_historical_data(name="NSE:" + name + "-EQ", interval=timeframe, timeperiod=3)
        df = pd.DataFrame()
        df = df.append(dx)
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)

        df['5ema'] = talib.EMA(df['close'], timeperiod=ema_period)

        trigger_candle = df.iloc[-3]
        signal_candle = df.iloc[-2]
        current_candle = df.iloc[-1]

        trigger_candle_formed = trigger_candle['close'] > (trigger_candle['low'] * 1.007)
        signal_candle_formed = signal_candle['low'] > signal_candle['5ema']
        sell_signal_formed = current_candle['low'] < signal_candle['low']

        if trigger_candle_formed and signal_candle_formed and sell_signal_formed and traded[name] is False:
            print(f"{Fore.YELLOW} Signal for {name} on {datetime.datetime.now().time()} {Fore.WHITE} \n")
            sl = trigger_candle['high'] if trigger_candle['high'] > signal_candle['high'] else signal_candle['high']

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
                    traded[name] = True

    except Exception as e:
        print(f"Error occurred : {e}")
        return

def getTradeTime():
    return datetime.time(9, 15) < datetime.datetime.now().time() < datetime.time(10, 30)

def ema5Strategy(watchlist):
    traded = {}
    for symbol in watchlist:
        traded[symbol] = False

    while getTradeTime():
        for name in watchlist:
            x = threading.Thread(target=process(name, traded), args=(2))
            print(f"Thread started for {name}")
            x.start()

def main():
    utility.fyers_login()

    watchlist = ['ACC', 'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'AMBUJACEM', 'APOLLOHOSP', 'ASIANPAINT', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJAJHLDNG', 'BAJFINANCE', 'BANDHANBNK', 'BANKBARODA', 'BERGEPAINT', 'BHARTIARTL', 'BIOCON', 'BOSCHLTD', 'BPCL', 'BRITANNIA', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COLPAL', 'DABUR', 'DIVISLAB', 'DLF', 'DMART', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GLAND', 'GODREJCP', 'GRASIM', 'HAVELLS', 'HCLTECH', 'HDFC', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO', 'HINDUNILVR', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'IGL', 'INDIGO', 'INDUSINDBK', 'INDUSTOWER', 'INFY', 'IOC', 'ITC', 'JINDALSTEL', 'JSWSTEEL', 'JUBLFOOD', 'KOTAKBANK', 'LT', 'LTI', 'LUPIN', 'MARICO', 'MARUTI', 'MCDOWELL-N', 'MUTHOOTFIN', 'M&M', 'NAUKRI', 'NMDC', 'NTPC', 'ONGC', 'PEL', 'PGHH', 'PIDILITIND', 'PIIND', 'PNB', 'POWERGRID', 'RELIANCE', 'SAIL', 'SBICARD', 'SBILIFE', 'SBIN', 'SHREECEM', 'SIEMENS', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'TORNTPHARM', 'ULTRACEMCO', 'UPL', 'VEDL', 'WIPRO', 'YESBANK']
    ema5Strategy(watchlist);

if __name__ == '__main__':
    main()




