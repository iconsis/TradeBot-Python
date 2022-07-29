
from colorama import Fore
import pandas as pd
import datetime
import time
import talib
import threading
import logging
from utilities import algo_util as utility

logger = logging.getLogger(__name__)

def process(name, status):
    risk_capacity = 100
    ema_period = 200
    rsi_period = 10
    timeframe = '5min'
    tgt_multiplier = 2
    traded = False

    while getTradeTime() and status['traded'] != 'yes':
        try:
            dx = utility.get_historical_data(name="NSE:" + name + "-EQ", interval=timeframe, timeperiod=3)
            df = pd.DataFrame()
            df = df.append(dx)

            df['200_ma'] = talib.EMA(df['close'], timeperiod=ema_period)
            df['rsi_10'] = talib.RSI(df['close'], timeperiod=rsi_period)

            trigger_candle = df.iloc[-3]
            signal_candle = df.iloc[-2]

            buy_signal_formed = signal_candle['rsi_10'] < 30 and trigger_candle['rsi_10'] > 30
            buy_signal_formed = buy_signal_formed and trigger_candle['close'] > trigger_candle['200_ma']
            buy_signal_formed = buy_signal_formed and signal_candle['close'] < signal_candle['open']

            if buy_signal_formed:
                logger.info(f"Signal for trade : {buy_signal_formed and traded is False} for {name}")
                logger.info(f"{Fore.YELLOW} Signal for {name} on {datetime.datetime.now().time()} {Fore.WHITE} \n")

                status['name'] = name
                status['state'] = 'Ready for buy'
                status['buy_sell'] = "buy"
                status['trade_date'] = signal_candle['date']
                status['entry_time'] = signal_candle['date'].time()
                status['entry_price'] = signal_candle['close']
                status['sl_price'] = status['entry_price'] - ((status['entry_price'] * 0.25) / 100)

                try:
                    qty = int(risk_capacity / (status['sl_price'] - status['entry_price']))
                except Exception as e:
                    logger.info(f"trade not taken for {name} as SL, entry values are not valid")
                    continue

                status['qty'] = qty
                if qty <= 0:
                    logger.info(f"trade not taken for {name} as SL value exceeds risk capacity")
                else:
                    sl_points = round((status['sl_price'] - status['entry_price']) * 20.0) / 20.0
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
                    logger.info(f"Response : {response}")
                    if response is not None:
                        status['traded'] = 'yes'
                        logger.info(f"Trade : {status}")

        except Exception as e:
            logger.info(f"Error occurred : {e}")
        time.sleep(3)

def getTradeTime():
    return datetime.time(9, 15) < datetime.datetime.now().time() < datetime.time(12, 00)

def rsi10ema200Strategy(watchlist):

    for name in watchlist:
        status = getEmptyStatusObject()
        x = threading.Thread(target=process, args=(name,status,))
        logger.info(f"Thread started for {name}")
        x.start()
        time.sleep(3)

def getEmptyStatusObject():
    return {
        'state': None,
        'buysell': None,
        'name': None,
        'sell_date': None,
        'entry_time': None,
        'entry_price': None,
        'signal_candle_date': None,
        'traded': None,
        'qty': None,
        'sl_price': None,
        'tg': None,
        'exit_time': None,
        'exit_price': None,
        'pnl': None,
        'target_hit': None,
        'sl_hit': None,
    }

