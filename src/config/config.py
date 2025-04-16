# src/config/config.py

import os

from dotenv import load_dotenv

load_dotenv()

class CONFIG:
    """
    Configuration class for backtest parameters.
    """

    LOOKBACK_DAYS = 90 #365
    DATA_TIMEFRAME = "1h"
    CCXT_DATA_SYMBOL = "BTC/USDT"
    BINANCE_DATA_SYMBOL = "BTCUSDT"  # Binance format

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
