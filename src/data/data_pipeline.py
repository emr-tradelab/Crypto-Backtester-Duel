import os
import time
from datetime import datetime, timedelta, timezone

import polars as pl

from config.config import CONFIG
from utils.utils import timeit

from .binance_api_downloader import BinanceDirectDownloader
from .ccxt_data_downloader import ccxtBinanceDataDownloader


def calc_dates():
    """Calculates the start and end timestamps in milliseconds for fetching
    historical data.

    Returns:
        tuple[int, int]: A tuple containing the start and end timestamps in
            milliseconds.
    """
    # fetch LOOKBACK_DAYS worth of data
    end_time = datetime.now(timezone.utc)
    print(f"End time: {end_time}")
    start_time = end_time - timedelta(days=CONFIG.LOOKBACK_DAYS)
    print(f"Start time: {start_time}")

    start_ms = int(time.mktime(start_time.timetuple()) * 1000)
    end_ms = int(time.mktime(end_time.timetuple()) * 1000)

    return start_ms, end_ms


@timeit
def ccxt_fetch():
    start_ms, end_ms = calc_dates()

    ccxt_client = ccxtBinanceDataDownloader(
        api_key=CONFIG.BINANCE_API_KEY, api_secret=CONFIG.BINANCE_API_SECRET
    )

    return ccxt_client.fetch_historical(
        symbol=CONFIG.CCXT_DATA_SYMBOL,
        timeframe=CONFIG.DATA_TIMEFRAME,
        start_ms=start_ms,
        end_ms=end_ms,
    )


@timeit
def binance_direct_fetch():
    start_ms, end_ms = calc_dates()

    direct_client = BinanceDirectDownloader(
        api_key=CONFIG.BINANCE_API_KEY, api_secret=CONFIG.BINANCE_API_SECRET
    )
    return direct_client.fetch_ohlcv(
        symbol=CONFIG.BINANCE_DATA_SYMBOL,  # Using "BTCUSDT" vs. "BTC/USDT"
        interval=CONFIG.DATA_TIMEFRAME,
        start_ms=start_ms,
        end_ms=end_ms,
    )


def save_tmp_data(df: pl.DataFrame, filename: str):
    """
    Save the DataFrame to a temporary file.
    """
    # Save the DataFrame to a temporary file
    df.write_parquet(filename)
    print(f"Temporary data saved to {filename}")


def load_tmp_data(filename: str) -> pl.DataFrame:
    """
    Load the DataFrame from a temporary file.
    """
    # Load the DataFrame from the temporary file
    df = pl.read_parquet(filename)
    print(f"Temporary data loaded from {filename}")
    return df


def get_historical_data(download=False):
    if download:
        print("\nStarting Direct Binance download ...")
        df_direct = binance_direct_fetch()

        os.makedirs(os.path.join(CONFIG.ROOT_PATH, "data"), exist_ok=True)
        save_tmp_data(df_direct, CONFIG.DATA_TMP_PATH)
    else:
        print("\nLoading Direct Binance data from tmp file ...")
        df_direct = load_tmp_data(CONFIG.DATA_TMP_PATH)

    print(f"Binance result: {df_direct.head()}")
    print(f"Binance result shape: {df_direct.shape}")
    return df_direct
