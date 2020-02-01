import twstock
import pickle
from functools import wraps
from time import time, sleep
import json
import requests
from requests.exceptions import ConnectionError
from setting import (
    STATIC_CODES, UPDATE_CODES_INTERVAL, LOGGER, StockInfoSetting)

def dump(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Dump {path}")

def read(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        LOGGER.info(f'[{f.__name__}] Elapsed time: {end-start}')
        return result
    return wrapper

def genStockList(output_file=None, force_update=False):
    if force_update:
        twstock.__update_codes()

    stocks = []
    for code in twstock.codes:
        stock =  twstock.codes[code]
        if stock.type == '股票':
            # stocks.append(f'{code},{stock.name}')
            # stocks.append((code, stock.name))
            stocks.append(code)
    
    LOGGER.info(f'Get {len(stocks)} stocks in list')
    return sorted(stocks)

def chunck_slice(array, chunck_size=100):
    n = 0 
    total = len(array)
    while n < total:
        yield array[n: n + chunck_size]
        n += chunck_size

def isStockCold(vol, upper=150, mean=100):
    vol_max = max(vol)
    vol_sum = sum(vol)
    vol_mean = vol_sum / len(vol)
    return vol_max < upper and vol_mean < mean

@timing
def getStockList(force_update=False):
    if force_update:
        twstock.__update_codes()

    stocks = []
    for code in twstock.codes:
        stock =  twstock.codes[code]
        if stock.type == '股票':
            stocks.append(stock)
    
    LOGGER.info(f'Get {len(stocks)} stocks in list')

    return stocks

def getStockInfo(stock_code):
    LOGGER.info(f"Processing {stock_code} ...")
    retry = 0
    stock = None
    while retry <= StockInfoSetting.RETRY_MAX_TIME and stock is None:
        try:
            stock = twstock.Stock(stock_code)
            break
        except ConnectionError:
            LOGGER.warning(f'Grab {stock_code} Fail, Retry ({retry}/{StockInfoSetting.RETRY_MAX_TIME})')
        except Exception:
            LOGGER.warning(f'Grab {stock_code} Fail, Retry ({retry}/{StockInfoSetting.RETRY_MAX_TIME})', exc_info=True)

        retry += 1
        sleep(1)

    return stock

@timing
def genColdList(codes=None, path=STATIC_CODES):
    lists = []
    if codes is None:
        codes = genStockList(force_update=True)

    for code in codes:
        stock = getStockInfo(code)
        
        # It'll get information in last 30 days
        if stock and isStockCold(stock.capacity):
            lists.append(code)
        sleep(0.5)
    with open(path, 'w') as f :
        json.dump(lists, f, ensure_ascii=False)
    return lists

@timing 
def loadColdList():
    if not STATIC_CODES.is_file() or \
        time() - STATIC_CODES.stat().st_mtime > UPDATE_CODES_INTERVAL:
        genColdList()
    return list(map(str, json.load(STATIC_CODES.open())))

@timing
def buildHistory(codes=None, force_update=False):
    import pandas as pd
    if codes is None:
        codes = genStockList(force_update=force_update)

    stock = twstock.Stock(codes[0])
    vols = pd.DataFrame({codes[0]: stock.capacity}, index=stock.date)
    for code in codes[1:]:
        stock = twstock.Stock(code)
        vols[code] = stock.capacity

    dump(vols, 'vol.pkl')

if __name__ == "__main__":
    # buildHistory()
    r = loadColdList()
    print(r)
