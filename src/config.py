# src/config/config.py

from pathlib import Path
from typing import Optional

from emrpy import get_root_path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Switches
    simple_bt_backtestpy: bool = True
    simple_bt_nautilus: bool = False

    # Data parameters
    lookback_days: int = 365
    data_timeframe: str = '1h'
    ccxt_data_symbol: str = 'BTC/USDT'
    binance_data_symbol: str = 'BTCUSDT'

    # Credentials (optional for public-market data requests)
    binance_api_key: Optional[str] = Field(default=None, env="BINANCE_API_KEY")
    binance_api_secret: Optional[str] = Field(default=None, env="BINANCE_API_SECRET")

    # Root path
    root_path: Path = Field(get_root_path(0))

    # Pydantic settings
    model_config = SettingsConfigDict(
        env_file=".env",   # load .env from project root
        extra="forbid"     # error on any unexpected vars
    )

    @property
    def tmp_filename(self) -> str:
        return (
            f"{self.binance_data_symbol}_"
            f"{self.data_timeframe}_"
            f"tmp_{self.lookback_days}days.parquet"
        )

    @property
    def data_tmp_path(self) -> str:
        return str(self.root_path / "data" / self.tmp_filename)

# Singleton-style instantiation
config = Settings()

if __name__ == "__main__":
    # quick smoke-test
    print("Root path:", config.root_path)
    print("Temp file path:", config.data_tmp_path)
