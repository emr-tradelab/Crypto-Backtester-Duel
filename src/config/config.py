# src/config/config.py

import os

from dotenv import load_dotenv
from emrpy import get_root_path

load_dotenv()


class CONFIG:
    """
    Configuration class for backtest parameters.
    """
    # Switches
    SIMPLE_BT_BACKTESTPY = True
    SIMPLE_BT_NAUTILUS = False

    # Data parameters
    LOOKBACK_DAYS = 365
    DATA_TIMEFRAME = "1h"
    CCXT_DATA_SYMBOL = "BTC/USDT"
    BINANCE_DATA_SYMBOL = "BTCUSDT"  # Binance format

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

    # Paths
    ROOT_PATH = get_root_path()
    TMP_FILENAME = f"{BINANCE_DATA_SYMBOL}_{DATA_TIMEFRAME}_tmp_{LOOKBACK_DAYS}days.parquet"
    DATA_TMP_PATH = os.path.join(ROOT_PATH, "data", TMP_FILENAME)

if __name__ == "__main__":

    print(CONFIG.ROOT_PATH)
