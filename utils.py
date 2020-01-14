import twstock
import pickle
from functools import wraps
from time import time, sleep
import numpy as np
import json
from config import STATIC_CODES, UPDATE_CODES_INTERVAL

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
        print(f'[{f.__name__}] Elapsed time: {end-start}')
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
    
    print(f'Get {len(stocks)} stocks in list')
    return stocks

def chunck_slice(array, chunck_size=100):
    n = 0 
    total = len(array)
    while n < total:
        yield array[n: n + chunck_size]
        n += chunck_size

def isStockCold(vol, upper=100, mean=80):
    vol = np.array(vol)
    if vol.max() > upper:
        return False
    if vol.mean() > mean:
        return False
    return True

@timing
def getStockList(force_update=False):
    if force_update:
        twstock.__update_codes()

    stocks = []
    for code in twstock.codes:
        stock =  twstock.codes[code]
        if stock.type == '股票':
            stocks.append(stock)
    
    print(f'Get {len(stocks)} stocks in list')

    return stocks


@timing
def genColdList(codes=None, path=STATIC_CODES, price_upper_bound=500):
    lists = []
    if codes is None:
        codes = genStockList(force_update=True)

    for code in codes:
        print(f"Processing {code} ...")
        stock = twstock.Stock(code)
        if isStockCold(stock.capacity):
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
    genColdList()