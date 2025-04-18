# src/main.py
import argparse
from emrpy.logutils.logger_config import configure, get_logger

from backtesting import Backtest
from data.data_pipeline import get_historical_data
from strategies.backtesting_py import SmaCross_bt
from utils.utils import polars_to_pandas
from config.config import CONFIG


# ────────────────────────── logger setup ────────────────────────────
configure(name="", level="INFO", filename="nautilus_bt.log")
log = get_logger(__name__)          # module‑level logger
# ────────────────────────────────────────────────────────────────────


def run_bt_sma_backtest(df_pl) -> None:
    df_pd = polars_to_pandas(df_pl)
    bt = Backtest(df_pd, SmaCross_bt, cash=1_000_000, commission=0.002)
    stats = bt.run()

    log.info("Back‑test finished:\n%s", stats)   # replaces print
    # bt.plot()   # plot remains optional


def main(download: bool = False) -> None:

    # Fetch historical data
    try:
        log.info("Fetching data; download=%s", download)
        df = get_historical_data(download=download)
    except Exception as e:
        log.error("An error occurred while fetching data: %s", e)
        return
    
    # Run backtesting.py
    if CONFIG.SIMPLE_BT_BACKTESTPY:
        #run_bt_sma_backtest(df)
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backtesting frameworks comparison")
    parser.add_argument(
        "--download",
        action="store_true",
        default=False,
        help="Download data from Binance API",
    )
    args = parser.parse_args()
    main(download=args.download)