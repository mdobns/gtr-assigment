"""
This is for maintaining the profile after given budget . This also handles buy or sell according to provided info
"""
class Profile:
    def __init__(self, budget):
        self.budget = float(budget)
        self.cash = float(budget)
        self.shares = 0.0
        self.entry_price = None

    def buy(self, price):
        price = float(price)
        self.shares = self.cash / price
        self.entry_price = price
        self.cash = float(self.cash-self.shares*price)
        print(f"Buy done at {price} of total share {self.shares}")

    def sell(self, price):
        price = float(price)
        pnl = self.shares * (price - self.entry_price)
        self.cash += self.shares * price
        self.shares = 0.0
        print(f"Sell done at {price} of total cash {self.cash}")

        return pnl

    def roi(self):
        return ((self.cash - self.budget) / self.budget) * 100, self.cash
