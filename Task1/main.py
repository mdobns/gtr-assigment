"""
This is the main class from where trading strategy could be applied for different company/coin
"""
import warnings
from Task1.strategies.MovingAverageSrategy import MovingAverageStrategy

# Ignore warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

if __name__ == "__main__":
    strategy = MovingAverageStrategy("BTC-USD", "2018-01-01", "2023-12-31", 500)
    strategy.run()
