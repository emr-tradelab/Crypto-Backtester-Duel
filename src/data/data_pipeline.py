import os
import time
from datetime import datetime, timedelta, timezone

import polars as pl
from emrpy.decorators import timer
from emrpy.logutils.logger_config import get_logger

from src.config.config import CONFIG

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

    start_time = end_time - timedelta(days=CONFIG.LOOKBACK_DAYS)
    log.debug("Start time calculated as %s", start_time)

    start_ms = int(time.mktime(start_time.timetuple()) * 1000)
    end_ms = int(time.mktime(end_time.timetuple()) * 1000)

    return start_ms, end_ms


@timer
def ccxt_fetch():
    log.info("Starting CCXT fetch for symbol %s with timeframe %s",
             CONFIG.CCXT_DATA_SYMBOL, CONFIG.DATA_TIMEFRAME)
    start_ms, end_ms = calc_dates()

    ccxt_client = ccxtBinanceDataDownloader(
        api_key=CONFIG.BINANCE_API_KEY,
        api_secret=CONFIG.BINANCE_API_SECRET
    )

    data = ccxt_client.fetch_historical(
        symbol=CONFIG.CCXT_DATA_SYMBOL,
        timeframe=CONFIG.DATA_TIMEFRAME,
        start_ms=start_ms,
        end_ms=end_ms,
    )
    log.info("CCXT fetch completed: %d records", len(data))
    return data


@timer
def binance_direct_fetch():
    log.info("Starting direct Binance fetch for symbol %s with interval %s",
             CONFIG.BINANCE_DATA_SYMBOL, CONFIG.DATA_TIMEFRAME)
    start_ms, end_ms = calc_dates()

    direct_client = BinanceDirectDownloader(
        api_key=CONFIG.BINANCE_API_KEY,
        api_secret=CONFIG.BINANCE_API_SECRET
    )
    data = direct_client.fetch_ohlcv(
        symbol=CONFIG.BINANCE_DATA_SYMBOL,
        interval=CONFIG.DATA_TIMEFRAME,
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

        os.makedirs(os.path.join(CONFIG.ROOT_PATH, "data"), exist_ok=True)
        save_tmp_data(df_direct, CONFIG.DATA_TMP_PATH)
    else:
        log.info("Loading Direct Binance data from temporary file...")
        df_direct = load_tmp_data(CONFIG.DATA_TMP_PATH)

    log.debug("Binance result head:\n%s", df_direct.head())
    log.info("Binance data shape: %s", df_direct.shape)

    return df_direct
