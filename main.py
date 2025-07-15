# src/main.py

import argparse

from backtesting import Backtest
from emrpy.logging import configure, get_logger

from src.config import config
from src.data.data_pipeline import get_historical_data
from src.strategies.backtesting_py import SmaCross_bt, optimize
from src.utils.utils import polars_to_pandas

# ────────────────────────── logger setup ────────────────────────────
configure(name="", level="INFO", filename="nautilus_bt.log")
log = get_logger(__name__)
# ────────────────────────────────────────────────────────────────────

def run_bt_simple_backtest(df_pd, optimize_trials: int) -> None:
    """
    Run either an Optuna optimization or a simple SMA cross backtest
    based on optimize_trials.
    """
    if optimize_trials > 0:
        log.info("Running SMA cross optimization: %d trials", optimize_trials)
        study = optimize(df_pd, trials=optimize_trials)
        log.info("Optimization completed; Pareto-optimal trials: %d", len(study.best_trials))
        for t in study.best_trials:
            log.info(
                "Trial #%d: Return=%.2f%%, Sharpe=%.2f, n_short=%d, n_long=%d",
                t.number, t.values[0], t.values[1],
                t.params['n_short'], t.params['n_long']
            )
    else:
        log.info("Running simple SMA cross backtest")
        bt = Backtest(
            df_pd,
            SmaCross_bt,
            cash=1_000_000,
            commission=0.002,
            exclusive_orders=True
        )
        stats = bt.run()
        print(stats)
        bt.plot(filename="results/plot.html", open_browser=False)


def main(download: bool = False, optimize_trials: int = 0) -> None:
    # Fetch historical data
    try:
        log.info("Fetching data; download=%s", download)
        df_pl = get_historical_data(download=download)
    except Exception as e:
        log.error("An error occurred while fetching data: %s", e)
        return

    if config.simple_bt_backtestpy:
        df_pd = polars_to_pandas(df_pl)
        run_bt_simple_backtest(df_pd, optimize_trials)
    else:
        log.info("Simple backtest is disabled in config.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backtesting frameworks comparison")
    parser.add_argument(
        "--download",
        action="store_true",
        default=False,
        help="Download data from Binance API",
    )
    parser.add_argument(
        "--optimize-bt-simple",
        type=int,
        default=0,
        help="Run Optuna optimization on SMA cross (number of trials)",
    )
    args = parser.parse_args()
    main(download=args.download, optimize_trials=args.optimize_bt_simple)
