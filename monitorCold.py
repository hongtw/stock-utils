import sys
import time
import twstock
import traceback
import telegram
import os
import pytz
from datetime import datetime
import json
from utils import loadColdList, chunck_slice
from requests.exceptions import ConnectionError
from goodInfo import GoodInfo
from setting import (
    TEST_MODE,
    STATIC_CODES,
    TELEGRAM_JSON_FILE,
    SLEEP_BETWEEN_EPOCH,
    SLEEP_BETWEEN_REQ,
    WEEK_AVG_TIMES, 
    VOLUMN_MINIMUM,
    LOGGER
)
TAIWAN_TIMEZONE = pytz.timezone('Asia/Taipei')

def getVol(stocks, code):
    try:
        return int(stocks[code]['realtime']['accumulate_trade_volume'])
    except:
        print("\nSome Error happen...", traceback.format_exc())
        return 0

def isVolGreaterThanThreshold(code, stock_info, df):
    week_avg = df.loc[code, 'week_avg_vol']
    half_month_avg = df.loc[code, 'half_month_avg_vol']
    realtime_vols = int(stock_info['realtime']['accumulate_trade_volume'])
    return  realtime_vols > VOLUMN_MINIMUM and \
            realtime_vols > week_avg * WEEK_AVG_TIMES and \
            realtime_vols > half_month_avg * WEEK_AVG_TIMES * 1.1

def isPriceGreaterThanOpen(stock_info):
    price = float(stock_info['realtime']['latest_trade_price'])
    threshold = float(stock_info['realtime']['open']) * 1.02  # 比開盤高 2% 
    return price >= threshold

def isStockBecomeHot(code, stock_info, df):
    return isPriceGreaterThanOpen(stock_info) and isVolGreaterThanThreshold(code, stock_info, df)

def getRealtimeInfo(code_list, entry_time):
    stocks = {'success': False}
    if entry_time == 3:
        return stocks

    try:
        LOGGER.info(f"Retry to grab realtime infomation ({entry_time}/2)")
        stocks = twstock.realtime.get(code_list)
    except KeyboardInterrupt:
        os._exit() 
    except ConnectionError:
        LOGGER.warning("Connection Fail...")
        stocks = getRealtimeInfo(code_list, entry_time + 1)
    except:
        LOGGER.exception("Fail to Get realtime info")

    return stocks

def load_telegram_json():
    try:
        return json.load(TELEGRAM_JSON_FILE.open())
    except:
        LOGGER.warning('Fail to load config of telegram', exc_info=True)
        return None

def is_taiwan_stock_opening():
    taiwan_now = datetime.now(tz=TAIWAN_TIMEZONE)
    return taiwan_now.weekday() < 5 and  taiwan_now.hour > 9 and taiwan_now.hour < 14

class Reporter:
    def __init__(self, telegram_json=None):
        self.stocks = {}
        self.bot = None
        self.chat_id = None
        self._init_telegram_bot(telegram_json)

    def _init_telegram_bot(self, telegram_json):
        if telegram_json is not None:
            self.bot = telegram.Bot(token=telegram_json['token'])
            self.chat_id = telegram_json['chat_id']
            self.push_to_telegram(f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] 盤中監測啟動!!")
    
    def push_to_telegram(self, msg):
        if self.bot is not None:
            self.bot.send_message(chat_id=self.chat_id, text=msg)
    
    def add(self, stock_info):
        code = stock_info['info']['code']
        if code not in self.stocks:
            self.stocks[code] = stock_info

            get_time = stock_info['info']['time']
            name = stock_info['info']['name']
            acc_vols = stock_info['realtime']['accumulate_trade_volume']
            latest_trade_price = stock_info['realtime']['latest_trade_price']
            output_msg = f'[{get_time}] {name}({code}),\n價 {latest_trade_price}, 量 {acc_vols}'
            self.stocks[code]['output'] = output_msg
            self.push_to_telegram(output_msg)

    def show(self):
        output_msg = '\n========= 即時熱門股 =========\n' + '\n'.join([self.stocks[code]['output'] for code in self.stocks])
        print(output_msg)    

def main():
    LOGGER.info(f"Loading stocks ...")
    telegram_json = load_telegram_json()
    reporter = Reporter(telegram_json)
    df = GoodInfo.output_cold_stocks()
    codes = df.index.tolist()
    total = len(codes)
    
    LOGGER.info(f"Get {total} Cold stocks")
    reporter.push_to_telegram(f'從 GoodInfo 抓到 {total} 筆冷門股')
    while True:
        if not (TEST_MODE or is_taiwan_stock_opening()):
            print("非開市時間..")
            time.sleep(SLEEP_BETWEEN_EPOCH)
            continue

        LOGGER.info(f"Monitoring {total} Cold stocks")
        try:
            for cs in chunck_slice(codes, chunck_size=20):
                # stocks = twstock.realtime.get(cs)
                stocks = getRealtimeInfo(cs, 0)
                if stocks['success'] == False: 
                    print("Fail!!!!!!")
                    continue
                
                for code in stocks:
                    print(f'{code} ,', end='')
                    if code not in cs or not stocks[code]['success']: continue
                    if isStockBecomeHot(code, stocks[code], df):
                        realtime = stocks[code]['realtime']
                        name = stocks[code]['info']['name']
                        LOGGER.info(f"**********[{name} {code}] is HOT (Price={realtime['latest_trade_price']}, Vol={realtime['accumulate_trade_volume']})!!!!***********")
                        reporter.add(stocks[code])
                        
                print('')
                reporter.show()
                time.sleep(SLEEP_BETWEEN_REQ)
        except KeyboardInterrupt:
            os._exit() 
        except:
            LOGGER.exception("\nSome Error happen...")

        print(f"\nSleep for {SLEEP_BETWEEN_EPOCH} seconds")
        time.sleep(SLEEP_BETWEEN_EPOCH)

if __name__ == "__main__":
    main()