class Indicator:
    @staticmethod
    def moving_average(df, column, window):
        return df[column].rolling(window=window).mean()
