# src/strategies/backtesting_py.py

import optuna
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA


class SmaCross_bt(Strategy):
    """
    A simple SMA Cross strategy:
    - Long when short SMA crosses above long SMA.
    - Close when short SMA crosses below long SMA.
    """
    n_short: int = 30
    n_long:  int = 100

    def init(self):
        price = self.data.Close
        self.sma_short = self.I(SMA, price, self.n_short)
        self.sma_long  = self.I(SMA, price, self.n_long)

    def next(self):
        if crossover(self.sma_short, self.sma_long):
            self.buy()
        elif crossover(self.sma_long, self.sma_short):
            self.position.close()

def optimize(df, trials: int = 100):
    """
    Optimize n_short and n_long using an Optuna multi-objective study
    maximizing Return [%] and Sharpe Ratio.
    """
    def objective(trial):
        # Suggest parameters
        n_short = trial.suggest_int('n_short', 5, 50)
        n_long  = trial.suggest_int('n_long', n_short + 1, 200)

        # Update strategy parameters
        SmaCross_bt.n_short = n_short
        SmaCross_bt.n_long  = n_long

        # Run backtest
        bt = Backtest(
            df,
            SmaCross_bt,
            cash=1_000_000,
            commission=0.002,
            exclusive_orders=True
        )
        stats = bt.run()

        # Return multi-objective metrics
        return stats['Return [%]'], stats['Sharpe Ratio']

    # Create and run study
    study = optuna.create_study(
        directions=['maximize', 'maximize'],
        study_name='sma_cross_multiobj'
    )
    study.optimize(objective, n_trials=trials)
    return study
