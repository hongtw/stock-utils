import time
import twstock
import traceback
from utils import loadColdList, chunck_slice
from config import (
    STATIC_CODES,
    SLEEP_BETWEEN_EPOCH,
    SLEEP_BETWEEN_REQ,
    VOL_THRESHOLD
)

def getVol(stocks, code):
    try:
        return int(stocks[code]['realtime']['accumulate_trade_volume'])
    except:
        print("\nSome Error happen...", traceback.format_exc())
        return 0

def isVolGreaterThanThreshold(stock_info):
    return int(stock_info['realtime']['accumulate_trade_volume']) > VOL_THRESHOLD

def isPriceGreaterThanOpen(stock_info):
    return stock_info['realtime']['latest_trade_price'] > stock_info['realtime']['open']

def isStockBecomeHot(stock_info):
    return isPriceGreaterThanOpen(stock_info) and isVolGreaterThanThreshold(stock_info)

def main():
    codes = loadColdList()
    while True:
        try:
            for cs in chunck_slice(codes, chunck_size=30):
                stocks = twstock.realtime.get(cs)
                if stocks['success'] == False: 
                    print("Fail!!!!!!")
                    continue
                
                for s in stocks:
                    if s not in cs or not stocks[s]['success']: continue
                    # print(s, getVol(stocks, s))
                    if isStockBecomeHot(stocks[s]):
                        print(f"\n**********[{s}] is HOT !!!!***********")

                time.sleep(SLEEP_BETWEEN_REQ)
        except:
            print("\nSome Error happen...", traceback.format_exc())

        print(f"\nSleep for {SLEEP_BETWEEN_EPOCH} seconds")
        time.sleep(SLEEP_BETWEEN_EPOCH)

if __name__ == "__main__":
    main()