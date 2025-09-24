import os
import time
from datetime import datetime, timedelta, timezone

import polars as pl
from emrpy.decorators import timer
from emrpy.logging import get_logger

from src.config import config

from .binance_api_downloader import BinanceDirectDownloader
from .ccxt_data_downloader import ccxtBinanceDataDownloader

log = get_logger(__name__)


def calc_dates():
    """Calculates the start and end timestamps in milliseconds for fetching
    historical data.

    Returns:
        tuple[int, int]: A tuple containing the start and end timestamps in
            milliseconds.
    """
    end_time = datetime.now(timezone.utc)
    log.debug("End time calculated as %s", end_time)

    start_time = end_time - timedelta(days=config.lookback_days)
    log.debug("Start time calculated as %s", start_time)

    start_ms = int(time.mktime(start_time.timetuple()) * 1000)
    end_ms = int(time.mktime(end_time.timetuple()) * 1000)

    return start_ms, end_ms


@timer
def ccxt_fetch():
    log.info("Starting CCXT fetch for symbol %s with timeframe %s",
             config.ccxt_data_symbol, config.data_timeframe)
    start_ms, end_ms = calc_dates()

    if not config.binance_api_key or not config.binance_api_secret:
        log.debug("Binance API credentials not provided; proceeding without authentication.")

    ccxt_client = ccxtBinanceDataDownloader(
        api_key=config.binance_api_key,
        api_secret=config.binance_api_secret
    )

    data = ccxt_client.fetch_historical(
        symbol=config.ccxt_data_symbol,
        timeframe=config.data_timeframe,
        start_ms=start_ms,
        end_ms=end_ms,
    )
    log.info("CCXT fetch completed: %d records", len(data))
    return data


@timer
def binance_direct_fetch():
    log.info("Starting direct Binance fetch for symbol %s with interval %s",
             config.binance_data_symbol, config.data_timeframe)
    start_ms, end_ms = calc_dates()

    if not config.binance_api_key or not config.binance_api_secret:
        log.debug("Binance API credentials not provided; proceeding without authentication.")

    direct_client = BinanceDirectDownloader(
        api_key=config.binance_api_key,
        api_secret=config.binance_api_secret
    )
    data = direct_client.fetch_ohlcv(
        symbol=config.binance_data_symbol,
        interval=config.data_timeframe,
        start_ms=start_ms,
        end_ms=end_ms,
    )
    log.info("Direct Binance fetch completed: %d records", len(data))
    return data


def save_tmp_data(df: pl.DataFrame, filename: str):
    """
    Save the DataFrame to a temporary file.
    """
    df.write_parquet(filename)
    log.info("Temporary data saved to %s", filename)


def load_tmp_data(filename: str) -> pl.DataFrame:
    """
    Load the DataFrame from a temporary file.
    """
    df = pl.read_parquet(filename)
    log.info("Temporary data loaded from %s", filename)
    return df


def get_historical_data(download=False):
    """Fetches or loads historical data based on the `download` flag."""
    if download:
        log.info("Starting Direct Binance download...")
        df_direct = binance_direct_fetch()

        os.makedirs(os.path.join(config.root_path, "data"), exist_ok=True)
        save_tmp_data(df_direct, config.data_tmp_path)
    else:
        log.info("Loading Direct Binance data from temporary file...")
        df_direct = load_tmp_data(config.data_tmp_path)

    log.debug("Binance result head:\n%s", df_direct.head())
    log.info("Binance data shape: %s", df_direct.shape)

    return df_direct
