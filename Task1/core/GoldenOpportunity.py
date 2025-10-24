"""
This helps to identify market movement
"""
import numpy as np


class GoldenOpportunityGenerator:
    """
    if market bullish it will mark it as 2,
    if bearish then -2 else 0 for neutral
    """

    def golden_opportumity(self, df):
        df['Signal'] = np.where(df['MA_50']>df['MA_200'],1,-1)
        df['Position_move'] = df['Signal'].diff()
        return df
