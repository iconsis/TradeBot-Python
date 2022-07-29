import threading
import time

from strategies.ema_5.ema_5_strategy_v2 import ema5Strategy
import logging

from strategies.rsi_10_ema_200.rsi_10_ema_200 import rsi10ema200Strategy
from utilities import algo_util as utility

logger = logging.getLogger(__name__)

def main():
    logger.info("Scheduler started... ")
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

    x = threading.Thread(target=ema5Strategy, args=(watchlist,))
    logger.info(f"Thread started for ema5Strategy strategy")
    x.start()
    time.sleep(3)

    x = threading.Thread(target=rsi10ema200Strategy, args=(watchlist,))
    logger.info(f"Thread started for rsi10ema200Strategy strategy")
    x.start()
    time.sleep(3)

if __name__ == '__main__':
    main()
