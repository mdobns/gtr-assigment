import yfinance as yf
import pandas as pd

class FetchData:
    def __init__(self, symbol, start, end):
        self.symbol =symbol
        self.start_date = start
        self.end_date = end

    def fetch_data(self):
        print(f"Started downloading data for {self.symbol}")
        df = yf.download(self.symbol , self.start_date , self.end_date,auto_adjust=False)


        df.reset_index(inplace=True)  #
        df.drop_duplicates(inplace=True)
        df.ffill(inplace=True)
        return df
