from pathlib import Path
import pandas as pd
from backtesting import Backtest
from src.strategies.backtesting_py import SmaCross_bt, optimize
import logging

# Module logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def run_bt_simple_backtest(df_pd: pd.DataFrame, optimize_trials: int) -> None:
    """
    Run either an Optuna optimization or a simple SMA cross backtest
    based on optimize_trials.
    """
    if optimize_trials > 0:
        logger.info("Running SMA cross optimization: %d trials", optimize_trials)
        study = optimize(df_pd, trials=optimize_trials)
        logger.info("Optimization completed; Pareto-optimal trials: %d", len(study.best_trials))
        for t in study.best_trials:
            logger.info(
                "Trial #%d: Return=%.2f%%, Sharpe=%.2f, n_short=%d, n_long=%d",
                t.number, t.values[0], t.values[1],
                t.params['n_short'], t.params['n_long']
            )
    else:
        logger.info(f"Running simple SMA cross backtest with {len(df_pd)} candles")
        bt = Backtest(
            data=df_pd,
            strategy=SmaCross_bt,
            cash=1_000_000,
            commission=0.002,
            exclusive_orders=True
        )
        stats = bt.run()
        print(stats)

        # Plot and save
        output_dir = Path("results")
        output_dir.mkdir(parents=True, exist_ok=True)
        bt.plot(filename=str(output_dir / "bt-py_plot.html"), open_browser=False)