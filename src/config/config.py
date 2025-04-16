# src/config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class CONFIG:
    """
    Configuration class for backtest parameters.
    """

    LOOKBACK_DAYS = 365
    DATA_TIMEFRAME = "1h"
    CCXT_DATA_SYMBOL = "BTC/USDT"
    BINANCE_DATA_SYMBOL = "BTCUSDT"  # Binance format

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

    # Paths
    CWD = os.path.abspath(os.path.dirname(__file__))
    ROOT_PATH = os.path.abspath(os.path.join(CWD, "..", ".."))
    TMP_FILENAME = f"{BINANCE_DATA_SYMBOL}_{DATA_TIMEFRAME}_tmp_data_lookback{LOOKBACK_DAYS}.parquet"
    DATA_TMP_PATH = os.path.join(ROOT_PATH, "data", TMP_FILENAME)