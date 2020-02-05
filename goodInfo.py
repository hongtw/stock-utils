import requests
import pandas as pd

class GoodInfo:
    冷門股 = 'https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FILTER_ITEM0=%E5%B9%B3%E5%9D%87%E6%8C%AF%E5%B9%85%28%25%29%E2%80%93%E8%BF%91%E5%8D%8A%E5%B9%B4&FILTER_VAL_S0=0&FILTER_VAL_E0=15&FILTER_ITEM1=%E5%B9%B3%E5%9D%87%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%25%29%E2%80%93%E8%BF%91%E4%B8%89%E5%80%8B%E6%9C%88&FILTER_VAL_S1=0&FILTER_VAL_E1=5&FILTER_ITEM2=%E5%B9%B3%E5%9D%87%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%25%29%E2%80%93%E8%BF%91%E4%B8%80%E5%80%8B%E6%9C%88&FILTER_VAL_S2=0&FILTER_VAL_E2=7&FILTER_ITEM3=%E5%B9%B3%E5%9D%87%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%25%29%E2%80%93%E8%BF%9110%E6%97%A5&FILTER_VAL_S3=0&FILTER_VAL_E3=7&FILTER_ITEM4=%E5%B9%B3%E5%9D%87%E6%88%90%E4%BA%A4%E9%87%8F%E9%80%B1%E8%BD%89%E7%8E%87%28%25%29%E2%80%93%E8%BF%915%E6%97%A5&FILTER_VAL_S4=0&FILTER_VAL_E4=7&FILTER_ITEM5=%E8%82%A1%E6%9C%AC+%28%E5%84%84%E5%85%83%29&FILTER_VAL_S5=1&FILTER_VAL_E5=50&FILTER_ITEM6=---%E8%AB%8B%E9%81%B8%E6%93%87%E9%81%8E%E6%BF%BE%E6%A2%9D%E4%BB%B6---&FILTER_VAL_S6=&FILTER_VAL_E6=&FILTER_ITEM7=%E5%9D%87%E7%B7%9A%E4%B9%96%E9%9B%A2%28%25%29%E2%80%93%E6%9C%88&FILTER_VAL_S7=-7&FILTER_VAL_E7=7&FILTER_ITEM8=%E5%9D%87%E7%B7%9A%E4%B9%96%E9%9B%A2%28%25%29%E2%80%93%E5%AD%A3&FILTER_VAL_S8=-7&FILTER_VAL_E8=7&FILTER_ITEM9=%E5%96%AE%E5%AD%A3%E6%8C%AF%E5%B9%85%28%25%29%E2%80%93%E7%95%B6%E5%AD%A3&FILTER_VAL_S9=0&FILTER_VAL_E9=12&FILTER_ITEM10=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29&FILTER_VAL_S10=5&FILTER_VAL_E10=200&FILTER_ITEM11=---%E8%AB%8B%E9%81%B8%E6%93%87%E9%81%8E%E6%BF%BE%E6%A2%9D%E4%BB%B6---&FILTER_VAL_S11=&FILTER_VAL_E11=&FILTER_RULE0=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RULE1=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RULE2=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RULE3=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RULE4=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RULE5=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E9%81%B8%E8%82%A1%E6%A2%9D%E4%BB%B6---&FILTER_RANK0=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E6%8E%92%E5%90%8D%E6%A2%9D%E4%BB%B6---&FILTER_RANK1=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E6%8E%92%E5%90%8D%E6%A2%9D%E4%BB%B6---&FILTER_RANK2=---%E8%AB%8B%E6%8C%87%E5%AE%9A%E6%8E%92%E5%90%8D%E6%A2%9D%E4%BB%B6---&FILTER_SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&FILTER_SHEET2=%E8%BF%9112%E6%97%A5%E6%88%90%E4%BA%A4%E9%87%8F%E4%B8%80%E8%A6%BD&FILTER_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FILTER_QUERY=%E6%9F%A5++%E8%A9%A2'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    TARGET_IDX = 56
    成交量倍數 = 5
    
    def __init__(self, create_cold_list=True):
        self.data = None

        if create_cold_list:
            self.data = self.output_cold_stocks()

    def get_codes(self):
        return self.data.index.tolist()

    def is_vol_greater_than_last_avg(self, code, realtime_vol):
        if self.data is None:
            raise ValueError('Stock Data is not built yet')
        if code not in self.data.index:
            return False
        return realtime_vol > self.data.loc[code, 'avg_vols'] * self.成交量倍數

    def get_vol_threshold(self, code):
        if self.data is None:
            raise ValueError('Stock Data is not built yet')
        if code not in self.data.index:
            return 0
        return self.data.loc[code, 'avg_vols'] * self.成交量倍數

    def is_stock_become_hot(self, code, realtime_vol):
        if self.data is None:
            raise ValueError('Stock Data is not built yet')
        if code not in self.data.index:
            return False
        
        return self.is_vol_greater_than_last_avg(code, realtime_vol)

    @classmethod
    def output_cold_stocks(cls):
        def parse_columns(df_cols):
            return list(map(lambda x: x[0], list(df_cols)))
    
        headers = {'User-Agent': cls.User_Agent}    
        page = requests.get(GoodInfo.冷門股, headers=headers)
        page.encoding = 'utf-8'
        df = pd.read_html(page.text)[cls.TARGET_IDX]
        
        cols = parse_columns(df.columns)
        df.columns = cols
        df['last'] = df.iloc[:, -2]
        df['week_avg_vol'] = df.iloc[:, 9:-1].mean(axis=1)
        df['week_max'] = df.iloc[:, 9:-1].max(axis=1)
        df['half_month_avg_vol'] = df.iloc[:, 4:-1].mean(axis=1)

        df['代號'] = df['代號'].astype(str)
        df.set_index('代號', inplace=True)
        return df

if __name__ == '__main__':
    stocks = GoodInfo.output_cold_stocks()
    print(stocks.shape)
    print(stocks.iloc[:5, [0, -3, -2, -1]])
    stocks.to_csv('goodinfo.csv')