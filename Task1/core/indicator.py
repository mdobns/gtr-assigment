"""
This is for calculating the moving average within given days
"""
class Indicator:
    @staticmethod
    def moving_average(df, column, window):
        return df[column].rolling(window=window).mean()
