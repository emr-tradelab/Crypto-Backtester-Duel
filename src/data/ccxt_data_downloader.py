import ccxt
import polars as pl
from datetime import datetime

class BinanceDataDownloader:
    def __init__(self, api_key=None, api_secret=None):
        """
        Initialize the Binance exchange object via CCXT.
        Keys optional for public data, but you can provide
        them if Binance imposes stricter rate limits.
        """
        self.exchange = ccxt.binance({
            "apiKey": api_key,
            "secret": api_secret
        })

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        limit: int = 500,
        since=None
    ) -> pl.DataFrame:
        """
        Fetch a small chunk of OHLCV data. If you need multiple years,
        you'll iterate in batches from 'since' forward.
        
        :param symbol: e.g. 'BTC/USDT'
        :param timeframe: e.g. '1m', '5m', '1h', '1d'
        :param limit: number of data points per fetch (max ~1000 for Binance)
        :param since: Millisecond timestamp to fetch from (optional)
        :return: A Polars DataFrame with columns [timestamp, open, high, low, close, volume].
        """
        raw_data = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, since=since)
        df = pl.DataFrame(
            raw_data,
            schema=["timestamp", "open", "high", "low", "close", "volume"],
            orient="row"
        )
        # Convert timestamp to a readable datetime
        df = df.with_columns(
            (pl.col("timestamp")).cast(pl.Datetime(time_unit="ms")).alias("timestamp")
        )
        return df

    def fetch_historical(
        self,
        symbol: str,
        timeframe: str,
        start_ms: int,
        end_ms: int,
        limit: int = 1000
    ) -> pl.DataFrame:
        """
        Fetch historical data in multiple chunks from start to end (in ms).
        Returns a concatenated Polars DataFrame.
        """
        all_data = []
        current_since = start_ms

        while True:
            chunk = self.fetch_ohlcv(symbol, timeframe, limit=limit, since=current_since)
            if chunk.is_empty():
                break
            all_data.append(chunk)
            # Move to the last timestamp + 1ms
            last_ts = chunk[-1, "timestamp"].timestamp()  # Polars -> Python datetime -> timestamp
            current_since = int(last_ts * 1000) + 1
            # If we've passed end_ms or chunk was smaller than limit, we can stop.
            if current_since > end_ms or len(chunk) < limit:
                break

        if not all_data:
            return pl.DataFrame()  # Return empty if no data
        
        return pl.concat(all_data)

