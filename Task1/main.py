from Task1.strategies.MovingAverageSrategy import MovingAverageStrategy
import warnings

# Suppress all warnings (optional, if you want a completely clean console)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

if __name__ == "__main__":
    strategy = MovingAverageStrategy("AMZN", "2024-01-01", "2025-10-20", 500)
    strategy.run()
