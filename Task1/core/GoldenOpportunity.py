import numpy as np


class GoldenOpportunityGenerator:
    def golden_opportumity(self, df):
        df['Signal'] = np.where(df['MA_50']>df['MA_200'],1,-1)
        df['Position_move'] = df['Signal'].diff()
        return df
