import time
import pyupbit
import datetime
import requests
import talib
import numpy as np
from pandas import Series

access = "ekwmasSfWWJ5GJx591PAVd3d8UhKoYd3GAwXvepm"
secret = "PgwvFxUDB01iZlxB6riDw5JrJ6InqpK6Uw3L2rF5"

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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

current_price = get_current_price("KRW-BTC")

url = "https://api.upbit.com/v1/candles/minutes/1"

querystring = {"market":"KRW-BTC","count":"200"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

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

#print()
#print('open_prices : {:,.2f}\n'.format(open_prices[-1]))
print('close_prices : {:,.2f}\n'.format(close_prices[-1]))
#print('high_prices : {:,.2f}\n'.format(high_prices[-1]))
#print('low_prices : {:,.2f}\n'.format(low_prices[-1]))

high_prices = np.array(high_prices, dtype='f8')
low_prices = np.array(low_prices, dtype='f8')
open_prices = np.array(open_prices, dtype='f8')
close_prices = np.array(close_prices, dtype='f8')

ma_1st = talib.SMA(close_prices, timeperiod=5)
ma_2nd = talib.SMA(close_prices, timeperiod=10)
ma_3rd = talib.SMA(close_prices, timeperiod=15)


#print('첫번째 이동평균선 : {:,.1f}'.format(ma_1st[-1]))
#print('두번째 이동평균선 : {:,.1f}'.format(ma_2nd[-1]))
#print('세번째 이동평균선 : {:,.1f}'.format(ma_3rd[-1]))

now_price = close_prices[-1]

MA1 = ma_1st[-1]
MA2 = ma_2nd[-1]
MA3 = ma_3rd[-1]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작


    # 현재가보다 이평선 시가가 모두 낮은 경우 매수
while True :
    try:
        krw = get_balance("KRW")
        btc = get_balance("BTC")
        # 현재가 > 전체 이평선 매수
        if now_price > MA1 and now_price > MA2 and now_price > MA3 :

            if MA1 > MA2 and MA2 > MA3 and MA1 > MA3 :
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                
        # 현재가 < 전체 이평선 매도
        elif now_price < MA1 and now_price < MA2 and now_price < MA3 :

            if MA1 < MA2 and MA2 > MA3 and MA1 > MA3 :
                if btc > 0.00009:
                    upbit.sell_market_order("KRW-BTC", btc)

        # 15일 선만 다른경우 매수-1
        elif now_price > MA1 and now_price > MA2 and now_price > MA3 :

            if MA1 > MA2 and MA2 < MA3 and MA1 < MA3 :
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)

        # 15일 선만 다른경우-매수2
        elif now_price > MA1 and now_price > MA2 and now_price < MA3 :

            if MA1 > MA2 and MA2 < MA3 and MA1 < MA3 :             
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)

        # 15일 선만 다른경우-매도2
        elif now_price < MA1 and now_price < MA2 and now_price > MA3 :
           
            if MA1 < MA2 and MA2 > MA3 and MA1 > MA3 :
                if btc > 0.00009:
                    upbit.sell_market_order("KRW-BTC", btc)
               
        else:
            print('현재 추세 전환 중 입니다.')

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)