"""
This is for running the strategy using the given parameters
"""

from Task1.core.data_fetcher import FetchData
from Task1.core.indicator import Indicator
from Task1.core.GoldenOpportunity import GoldenOpportunityGenerator
from Task1.core.profile import Profile

class MovingAverageStrategy:
    def __init__(self, symbol, start,end, budget):
        self.symbol =symbol
        self.start_date = start
        self.end_date =end
        self.budget =budget

    def run(self):
        fetcher = FetchData(self.symbol,self.start_date,self.end_date)
        df = fetcher.fetch_data()

        df['MA_50'] = Indicator.moving_average(df,'Close',50)
        df['MA_200'] = Indicator.moving_average(df,'Close',200)

        df = GoldenOpportunityGenerator().golden_opportumity(df)

        profile = Profile(self.budget)

        for i in range(200,len(df)):
            row = df.iloc[i]
            if int(row['Position_move']) ==2 and profile.shares ==0:
                profile.buy(row['Close'])

            elif int(row['Position_move']) == -2 and profile.shares !=0:
                pnl =float(profile.sell(row['Close']))
                print(f"Trade pnl: {pnl}({float(profile.roi()):.2f}%)")

        if profile.shares > 0:
            row = df.iloc[-1]
            print(f"Forcefully closed")
            pnl = float(profile.sell(row['Close']))

        print(f"Final ROI: {float(profile.roi()):.2f}%")



