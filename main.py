# src/main.py

import argparse
from emrpy.logging import configure, get_logger

from src.config import config
from src.data.data_pipeline import get_historical_data
from src.utils.utils import polars_to_pandas

# ────────────────────────── logger setup ────────────────────────────
configure(name="", level="INFO", filename="crypto-bt-duel.log")
log = get_logger(__name__)
# ────────────────────────────────────────────────────────────────────

def main(download: bool = False, optimize_trials: int = 0) -> None:
    # Fetch historical data
    try:
        log.info("Fetching data; download=%s", download)
        df_pl = get_historical_data(download=download)
    except Exception as e:
        log.error("An error occurred while fetching data: %s", e)
        return

    # backtesting.py backtest
    if config.simple_bt_backtestpy:
        from src.runners.backtesting_py import run_bt_simple_backtest

        df_pd = polars_to_pandas(df_pl)
        run_bt_simple_backtest(df_pd, optimize_trials)
    else:
        log.info("Simple backtest is disabled in config.")

    # NautilusTrader backtest
    if config.simple_bt_nautilus:
        from src.runners.nautilus_node import run_nautilus_simple_backtest
        from nautilus_trader.persistence.catalog import ParquetDataCatalog
        from pathlib import Path

        CATALOG_PATH = Path.cwd() / "catalog"
        CATALOG_PATH.mkdir(parents=True, exist_ok=True)

        results, engine = run_nautilus_simple_backtest(
            df=df_pl,
            catalog_path=CATALOG_PATH,
            include_ema_example=True,
            include_local_sma=False, # This is my manual simplified long-only SMA strategy
        )
        print(results)

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
