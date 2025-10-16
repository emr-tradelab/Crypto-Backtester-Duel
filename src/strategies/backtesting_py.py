# src/strategies/backtesting_py.py

import logging
import optuna
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


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
        logger.debug("Initialized SMA indicators: n_short=%s n_long=%s", self.n_short, self.n_long)

    def next(self):
        if crossover(self.sma_short, self.sma_long):
            logger.debug("Crossover detected: short->long at index %s", len(self.data.Close) - 1)
            self.buy()
        elif crossover(self.sma_long, self.sma_short):
            logger.debug("Crossover detected: long->short at index %s", len(self.data.Close) - 1)
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
        logger.debug("Running backtest trial n_short=%s n_long=%s", n_short, n_long)
        stats = bt.run()
        logger.debug("Backtest finished: Return[%%]=%s Sharpe=%s", stats.get('Return [%]'), stats.get('Sharpe Ratio'))

        # Return multi-objective metrics
        return stats['Return [%]'], stats['Sharpe Ratio']

    logger.info("Starting optuna study 'sma_cross_multiobj' with %s trials", trials)
    # Create and run study
    study = optuna.create_study(
        directions=['maximize', 'maximize'],
        study_name='sma_cross_multiobj'
    )
    study.optimize(objective, n_trials=trials)
    logger.info("Optuna study completed: trials=%s", len(study.trials))
    return study
