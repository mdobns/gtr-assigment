from Task1.strategies.MovingAverageSrategy import MovingAverageStrategy
import warnings

# Suppress all warnings (optional, if you want a completely clean console)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

if __name__ == "__main__":
    # class_Name(“AAPL”, ”2018 - 01 - 01”, ”2023 - 12 - 31”)
    strategy = MovingAverageStrategy("AAPL", "2018-01-01", "2023-12-31", 500)
    strategy.run()
