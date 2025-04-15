import time
from datetime import datetime, timezone, timedelta
from config.config import CONFIG
from data.ccxt_data_downloader import BinanceDataDownloader

def main():

    downloader = BinanceDataDownloader(
        api_key=CONFIG.BINANCE_API_KEY,
        api_secret=CONFIG.BINANCE_API_SECRET
    )

    # Example: fetch last LOOKBACK_DAYS worth of data
    end_time = datetime.now(timezone.utc)
    print(f"End time: {end_time}")
    start_time = end_time - timedelta(days=CONFIG.LOOKBACK_DAYS)
    print(f"Start time: {start_time}")

    start_ms = int(time.mktime(start_time.timetuple()) * 1000)
    end_ms = int(time.mktime(end_time.timetuple()) * 1000)

    df = downloader.fetch_historical(
        symbol=CONFIG.DATA_SYMBOL,
        timeframe=CONFIG.DATA_TIMEFRAME,
        start_ms=start_ms,
        end_ms=end_ms,
        limit=1000
    )

    if df.is_empty():
        print("No data returned.")
    else:
        print(f"Fetched {df.height} rows from {CONFIG.DATA_SYMBOL} - {CONFIG.DATA_TIMEFRAME}")
        print(df.head())  # Quick peek
        print(df.shape)

if __name__ == "__main__":
    main()
