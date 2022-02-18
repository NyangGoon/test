import time
import pyupbit
import datetime
import requests
import talib
import numpy as np
from pandas import Series

access = "ekwmasSfWWJ5GJx591PAVd3d8UhKoYd3GAwXvepm"
secret = "PgwvFxUDB01iZlxB6riDw5JrJ6InqpK6Uw3L2rF5"


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작

    # 현재가보다 이평선 시가가 모두 낮은 경우 매수
while True :
    try:
        url = "https://api.upbit.com/v1/candles/minutes/1"

        querystring = {"market":"KRW-BTC","count":"200"}

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, params=querystring)

        btc_price = response.json()

        open_prices = []
        close_prices = []
        high_prices = []
        low_prices = []

        for p in btc_price:
            open_prices.append(p['opening_price'])
            close_prices.append(p['trade_price'])
            high_prices.append(p['high_price'])
            low_prices.append(p['low_price'])
        open_prices.reverse() #reverse 역방향으로 재배열 
        close_prices.reverse()
        high_prices.reverse()
        low_prices.reverse() 
        close_prices = np.array(close_prices, dtype='f8')

        now_price = close_prices[-1]

        ma_1st = talib.SMA(close_prices, timeperiod=5)
        ma_2nd = talib.SMA(close_prices, timeperiod=10)
        ma_3rd = talib.SMA(close_prices, timeperiod=15)

        MA1 = ma_1st[-1]
        MA2 = ma_2nd[-1]
        MA3 = ma_3rd[-1]
        
        def get_balance(ticker):
            """잔고 조회"""
            balances = upbit.get_balances()
            for b in balances:
                if b['currency'] == ticker:
                    if b['balance'] is not None:
                        return float(b['balance'])
                    else:
                        return 0
            return 0

        time.sleep(2)

        krw = get_balance("KRW")
        btc = get_balance("BTC")
        # 현재가 > 전체 이평선 매수1
        if now_price > MA1 and now_price > MA2 and now_price > MA3 and MA1 >= MA2 and MA2 > MA3 and MA1 > MA3 :

            if krw > 5000:
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
    
        # 15일 선만 다른경우 매수2
        elif now_price > MA1 and now_price > MA2 and now_price > MA3 and MA1 >= MA2 and MA2 > MA3 and MA1 < MA3 :

            if krw > 5000:
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
               

        # 15일 선만 다른경우-매수3
        elif now_price > MA1 and now_price > MA2 and now_price < MA3 and MA1 >= MA2 and MA2 < MA3 and MA1 < MA3 :
          
            if krw > 5000:
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
               

        # 현재가 < 전체 이평선 매도1
        elif now_price < MA1 and now_price < MA2 and now_price < MA3 and MA1 <= MA2 and MA2 > MA3 and MA1 > MA3 :

            if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc)
               
        # 15일 선만 다른경우-매도2
        elif now_price < MA1 and now_price < MA2 and now_price > MA3 and MA1 <= MA2 and MA2 > MA3 and MA1 > MA3 :
           
            if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc)
                

        # 15일 선만 다른경우-매도3
        elif now_price > MA1 and now_price > MA2 and now_price > MA3 and MA1 <= MA2 and MA2 < MA3 and MA1 < MA3 :
             if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc)

        # 매도4
        elif now_price < MA1 and now_price < MA2 and now_price < MA3 and MA1 <= MA2 and MA2 < MA3 and MA1 < MA3 :
            
            if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc)
               
        else:
            continue

        time.sleep(2)
            
    except Exception as e:
        print(e)
        time.sleep(1)