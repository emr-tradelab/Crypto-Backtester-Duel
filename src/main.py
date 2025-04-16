# src/main.py
import time
from datetime import datetime, timedelta, timezone

from config.config import CONFIG
from data.binance_api_downloader import BinanceDirectDownloader
from data.ccxt_data_downloader import ccxtBinanceDataDownloader
from utils.utils import timeit


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

# @timeit
# def ccxt_fetch(start_ms, end_ms):
#     ccxt_client = ccxtBinanceDataDownloader(
#         api_key=CONFIG.BINANCE_API_KEY, api_secret=CONFIG.BINANCE_API_SECRET
#     )

#     return ccxt_client.fetch_historical(
#         symbol=CONFIG.CCXT_DATA_SYMBOL,
#         timeframe=CONFIG.DATA_TIMEFRAME,
#         start_ms=start_ms,
#         end_ms=end_ms,
#     )

@timeit
def binance_direct_fetch(start_ms, end_ms):
    direct_client = BinanceDirectDownloader(
        api_key=CONFIG.BINANCE_API_KEY, api_secret=CONFIG.BINANCE_API_SECRET
    )
    return direct_client.fetch_ohlcv(
        symbol=CONFIG.BINANCE_DATA_SYMBOL,  # Using "BTCUSDT" vs. "BTC/USDT"
        interval=CONFIG.DATA_TIMEFRAME,
        start_ms=start_ms,
        end_ms=end_ms,
    )

def main():
    START, END = calc_dates()

    # print("Starting CCXT fetch ...")
    # df_ccxt = ccxt_fetch(START, END)
    # print(f"CCXT result: {df_ccxt.head()}")
    # print(f"CCXT result shape: {df_ccxt.shape}")

    print("\nStarting Direct Binance fetch ...")
    df_direct = binance_direct_fetch(START, END)
    print(f"Direct Binance result: {df_direct.head()}")
    print(f"Direct Binance result shape: {df_direct.shape}")

if __name__ == "__main__":
    main()
