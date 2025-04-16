# src/main.py

import argparse

from backtesting import Backtest

from data.data_pipeline import get_historical_data
from strategies.backtesting_py import SmaCross_bt
from utils.utils import polars_to_pandas


def run_bt_sma_backtest(df_pl):
    # Convert to pandas DataFrame
    df_pd = polars_to_pandas(df_pl)

    # Create and run the backtest
    bt = Backtest(df_pd, SmaCross_bt, cash=1_000_000, commission=0.002)
    stats = bt.run()
    print(stats)

    # plot the results
    # bt.plot()


def main(download=False):
    df = get_historical_data(download=download)
    run_bt_sma_backtest(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backtesting frameworks comparison")
    parser.add_argument(
        "--download",
        action="store_true",
        default=False,
        help="Download data from Binance API",
    )
    args = parser.parse_args()

    # Pass the download argument to the main function
    main(download=args.download)
