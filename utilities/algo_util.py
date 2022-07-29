import warnings
from fyers_api import accessToken, fyersModel
import requests
import pandas as pd
import datetime
import time
import mibian
from utilities import fyers_login as flogin
import logging

logger = logging.getLogger(__name__)

step_values = {'BANKNIFTY':100, 'NIFTY':50, 'AARTIIND': 20, 'ACC': 20, 'ADANIENT': 20, 'ADANIPORTS': 10, 'ALKEM': 20, 'AMARAJABAT': 10, 'AMBUJACEM': 5, 'APLLTD': 10, 'APOLLOHOSP': 50, 'APOLLOTYRE': 5, 'ASHOKLEY': 2.5, 'ASIANPAINT': 20, 'AUBANK': 20, 'AUROPHARMA': 10, 'AXISBANK': 10, 'BAJAJ-AUTO': 50, 'BAJAJFINSV': 100, 'BAJFINANCE': 100, 'BALKRISIND': 20, 'BANDHANBNK': 5, 'BANKBARODA': 2.5, 'BATAINDIA': 20, 'BEL': 2.5, 'BERGEPAINT': 10, 'BHARATFORG': 10, 'BHARTIARTL': 10, 'BHEL': 1, 'BIOCON': 5, 'BOSCHLTD': 250, 'BPCL': 10, 'BRITANNIA': 20, 'CADILAHC': 5, 'CANBK': 5, 'CHOLAFIN': 10, 'CIPLA': 10, 'COALINDIA': 2.5, 'COFORGE': 50, 'COLPAL': 20, 'CONCOR': 10, 'CUB': 2.5, 'CUMMINSIND': 20, 'DABUR': 5, 'DEEPAKNTR': 20, 'DIVISLAB': 50, 'DLF': 5, 'DRREDDY': 50, 'EICHERMOT': 50, 'ESCORTS': 20, 'EXIDEIND': 2.5, 'FEDERALBNK': 1, 'GAIL': 2.5, 'GLENMARK': 5, 'GMRINFRA': 1, 'GODREJCP': 10, 'GODREJPROP': 20, 'GRANULES': 5, 'GRASIM': 20, 'GUJGASLTD': 10, 'HAVELLS': 20, 'HCLTECH': 10, 'HDFC': 50, 'HDFCAMC': 50, 'HDFCBANK': 20, 'HDFCLIFE': 10, 'HEROMOTOCO': 50, 'HINDALCO': 5, 'HINDPETRO': 5, 'HINDUNILVR': 20, 'IBULHSGFIN': 5, 'ICICIBANK': 10, 'ICICIGI': 20, 'ICICIPRULI': 5, 'IDEA': 1, 'IDFCFIRSTB': 1, 'IGL': 10,
               'INDIGO': 20, 'INDUSINDBK': 20, 'INDUSTOWER': 5, 'INFY': 20, 'IOC': 1, 'IRCTC': 20, 'ITC': 2.5, 'JINDALSTEL': 10, 'JSWSTEEL': 5, 'JUBLFOOD': 50, 'KOTAKBANK': 20, 'L&TFH': 2.5, 'LALPATHLAB': 50, 'LICHSGFIN': 10, 'LT': 20, 'LTI': 100, 'LTTS': 50, 'LUPIN': 20, 'M&M': 10, 'M&MFIN': 5, 'MANAPPURAM': 2.5, 'MARICO': 5, 'MARUTI': 100, 'MCDOWELL-N': 5, 'MFSL': 20, 'MGL': 20, 'MINDTREE': 20, 'MOTHERSUMI': 5, 'MPHASIS': 20, 'MRF': 500, 'MUTHOOTFIN': 20, 'NAM-INDIA': 5, 'NATIONALUM': 1, 'NAUKRI': 100, 'NAVINFLUOR': 50, 'NESTLEIND': 100, 'NMDC': 2.5, 'NTPC': 1, 'ONGC': 2.5, 'PAGEIND': 500, 'PEL': 50, 'PETRONET': 5, 'PFC': 2.5, 'PFIZER': 50, 'PIDILITIND': 20, 'PIIND': 20, 'PNB': 1, 'POWERGRID': 2.5, 'PVR': 20, 'RAMCOCEM': 10, 'RBLBANK': 5, 'RECLTD': 2.5, 'RELIANCE': 20, 'SAIL': 2.5, 'SBILIFE': 10, 'SBIN': 5, 'SHREECEM': 500, 'SIEMENS': 20, 'SRF': 100, 'SRTRANSFIN': 20, 'SUNPHARMA': 10, 'SUNTV': 10, 'TATACHEM': 10, 'TATACONSUM': 10, 'TATAMOTORS': 5, 'TATAPOWER': 2.5, 'TATASTEEL': 10, 'TCS': 50, 'TECHM': 20, 'TITAN': 20, 'TORNTPHARM': 20, 'TORNTPOWER': 5, 'TRENT': 20, 'TVSMOTOR': 10, 'UBL': 20, 'ULTRACEMCO': 100, 'UPL': 10, 'VEDL': 5, 'VOLTAS': 20, 'WIPRO': 5, 'ZEEL': 5}

warnings.filterwarnings("ignore")

def fyers_login():
    try:
        global fyers;

        access_token = flogin.get_access_token()
        print(access_token)
        fyers = fyersModel.FyersModel(token=access_token, is_async=False, client_id=flogin.client_id)
        logger.info(f"Login successful")
    except Exception as e:
        logger.info(f"Error in login : {e}")

def generate_access_token(auth_code, appId, secret_key):
    # creating an instance appSession by passing app id,secret key and redirect url as parameter
    appSession = accessToken.SessionModel(client_id=appId, secret_key=secret_key,grant_type="authorization_code")

    # we need to pass the auth code in set_token method
    appSession.set_token(auth_code)
    # generate_token function will return us the access token and we store in variable "access_token"
    access_token = appSession.generate_token()
    return access_token

def get_instruments():
    global instrument_df
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    request = requests.get(url=url, verify=False)
    data = request.json()
    instrument_df = pd.DataFrame(data)
    instrument_df.to_csv("instruments.csv")
    instrument_df.set_index("symbol", inplace=True)
    return instrument_df

def get_token_and_exchange(name):
    symboltoken = instrument_df.loc[name]['name']
    exchange = instrument_df.loc[name]['exch_seg']
    return symboltoken, exchange


def get_ohlc(name, exchange):
    symboltoken = instrument_df.loc[name]['token']
    ohlc_data = fyers.ltpData(exchange, name, symboltoken)
    ohlc_data = ohlc_data['data']
    return ohlc_data


def get_ltp(name, exchange):
    symboltoken = instrument_df.loc[name]['token']
    ltp_data = fyers.ltpData(exchange, name, symboltoken)
    ltp = ltp_data['data']['ltp']
    return ltp


def lot_size(name):
    lot = instrument_df.loc[name]['lotsize']
    return lot


def get_historical_data(name, interval, timeperiod):
    time.sleep(3)
    try:
        intervals_dict = {'1min': '1', '3min': '3', '5min': '5', '10min': '10', '15min': '15', '30min': '30', 'hour': '60', 'day': 'D'}
        todate = str(datetime.datetime.now().date())
        from_date = str(datetime.datetime.now().date() - datetime.timedelta(days=timeperiod))
        historicParam = {"symbol": name, "resolution": intervals_dict[interval], "date_format": "1", "range_from": from_date, "range_to": todate, "cont_flag": "1"}
        nx = fyers.history(historicParam)
        logger.info(f"History Response for {name} : {nx['s']}")
        if nx is not None:
            cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame.from_dict(nx['candles'])
            df.columns = cols
            df['date'] = pd.to_datetime(df['date'], unit="s")
            df['date'] = df['date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
            df['date'] = df['date'].dt.tz_localize(None)
            #df = df.set_index('date')
        else:
            logger.info(f"Error occurred while getting history data : {nx}")
        return df
    except Exception as e:
        logger.info(f"Error occurred while getting history data : {e}")

def get_ks_historical_data(name, interval, timeperiod):
    time.sleep(3)
    try:
        intervals_dict = {'1min': '1', '3min': '3', '5min': '5', '10min': '10', '15min': '15', '30min': '30', 'hour': '60', 'day': 'D'}
        todate = str(datetime.datetime.now().date())
        from_date = str(datetime.datetime.now().date() - datetime.timedelta(days=timeperiod))
        historicParam = {"symbol": name, "resolution": intervals_dict[interval], "date_format": "1", "range_from": from_date, "range_to": todate, "cont_flag": "1"}
        nx = fyers.history(historicParam)
        print(f"History Response for {name} : {nx['s']}")
        if nx is not None:
            cols = ['date', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame.from_dict(nx['candles'])
            df.columns = cols
            df['date'] = pd.to_datetime(df['date'], unit="s")
            df['date'] = df['date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
            df['date'] = df['date'].dt.tz_localize(None)
            #df = df.set_index('date')
        else:
            print(f"Error occurred while getting history data : {nx}")
        return df
    except Exception as e:
        print(f"Error occurred while getting history data : {e}")

def historical_bydate(symbol,sd,ed, interval = 1):
    data = {"symbol":symbol, "resolution":"5","date_format":"1","range_from":str(sd),"range_to":str(ed),"cont_flag":"1"}
    nx = fyers.history(data)
    cols = ['date','open','high','low','close','volume']
    df = pd.DataFrame.from_dict(nx['candles'])
    df.columns = cols
    df['date'] = pd.to_datetime(df['date'],unit = "s")
    df['date'] = df['date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['date'] = df['date'].dt.tz_localize(None)
    df = df.set_index('date')
    return df

def place_order(orderparams):
    time.sleep(1)
    orderId = fyers.place_order(orderparams)
    print("order is placed with orderid= ", orderId)
    return orderId

def option_name_finder(multiplier, name, exipry, ce_pe):
    temp_name = name.split("-")[0]
    ltp = get_ltp(name=name, exchange='NSE')
    step_value = step_values[temp_name]
    atm_strike = round(ltp/step_value)*step_value + multiplier*step_value
    option_name = temp_name + exipry + str(atm_strike) + 'CE'
    return option_name

def make_straddle(name, exipry, gap):
    ltp = get_ltp(name, "NSE")
    atm_strike = round(ltp/gap)*gap
    call_name = name + exipry + str(atm_strike) + 'CE'
    put_name = name + exipry + str(atm_strike) + 'PE'
    return [call_name, put_name]

def get_combined_premium(call_orderId, put_orderId):
    orders = pd.DataFrame(fyers.orderbook(['data']))

    call_avg_price = float(orders.loc[orders['orderid'] == call_orderId]['averageprice'])
    put_avg_price = float(orders.loc[orders['orderid'] == put_orderId]['averageprice'])

    combined_premium = call_avg_price + put_avg_price

    return combined_premium

def get_current_premium(call_script, put_script):
    call_ltp= get_ltp(call_script,"NFO")
    put_ltp= get_ltp(put_script,"NFO")
    current_premium = call_ltp + put_ltp
    return current_premium

def get_option_greeks(name, call_strike, put_strike, expiry):
    underlying_price = get_ltp(name=name,exchange="NSE")
    underlying_name = name.split("-")[0]
    call_script = underlying_name+ expiry +str(call_strike)+"CE"
    put_script = underlying_name+ expiry +str(put_strike)+"PE"
    call_price = get_ltp(name=call_script,exchange="NFO")
    put_price = get_ltp(name=put_script,exchange="NFO")
    interest_rate = 7
    days_to_expiry = 20

    civ = mibian.BS([underlying_price, call_strike, interest_rate, days_to_expiry], callPrice= call_price)
    print("Greeks for: ", "\t" ,call_script)
    print("IV :" , "\t\t" ,civ.impliedVolatility)

    cval = mibian.BS([underlying_price, call_strike, interest_rate, days_to_expiry],volatility = civ.impliedVolatility ,callPrice= call_price)
    print("callPrice: ", "\t" , cval.callPrice)
    print("callDelta: ", "\t" , cval.callDelta)
    print("callTheta: ", "\t" , cval.callTheta)
    print("vega: ", "\t\t" , cval.vega)
    print("gamma: ", "\t" , cval.gamma)
    print("\n","-------------------------------------------------------------------","\n")

    piv = mibian.BS([underlying_price, put_strike, interest_rate, days_to_expiry], putPrice= put_price)
    print("Greeks for: ", "\t" , put_script)
    print("IV : ", "\t\t" , piv.impliedVolatility)

    pval = mibian.BS([underlying_price, put_strike, interest_rate, days_to_expiry],volatility = piv.impliedVolatility ,putPrice= put_price)
    print("callPrice: ", "\t" , pval.callPrice)
    print("callDelta: ", "\t" , pval.callDelta)
    print("callTheta: ", "\t" , pval.callTheta)
    print("vega: ", "\t\t" , pval.vega)
    print("gamma: ", "\t" , pval.gamma)




