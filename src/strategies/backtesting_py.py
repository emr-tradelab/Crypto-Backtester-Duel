import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class SmaCross_bt(Strategy):
    """
    A simple SMA Cross strategy:
    - If short SMA crosses above long SMA, enter a long position.
    - If short SMA crosses below long SMA, close the position.
    """
    n_short = 10
    n_long = 20

    def init(self):
        # Convert the series to indicators used by backtesting.py
        price = self.data.Close
        self.sma_short = self.I(SMA, price, self.n_short)
        self.sma_long = self.I(SMA, price, self.n_long)

    def next(self):
        # If short SMA crosses above long SMA, and not already in a trade:
        if crossover(self.sma_short, self.sma_long):
            self.buy()

        # If short SMA crosses below long SMA, close any open position:
        elif crossover(self.sma_long, self.sma_short):
            self.position.close()
