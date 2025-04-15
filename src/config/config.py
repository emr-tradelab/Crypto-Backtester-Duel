# src/config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class CONFIG:
    """
    Configuration class for backtest parameters.
    """
    LOOKBACK_DAYS = 1 #365
    DATA_TIMEFRAME = "1h"
    DATA_SYMBOL = "BTC/USDT"

    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
