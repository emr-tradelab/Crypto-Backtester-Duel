# src/config/config.py

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from emrpy import get_root_path


class Settings(BaseSettings):
    # Switches
    simple_bt_backtestpy: bool = True
    simple_bt_nautilus: bool = False

    # Data parameters
    lookback_days: int = 365
    data_timeframe: str = '1h'
    ccxt_data_symbol: str = 'BTC/USDT'
    binance_data_symbol: str = 'BTCUSDT'

    # Credentials (not required for this example)
    # binance_api_key: str = Field(default="BINANCE_API_KEY", env="BINANCE_API_KEY")
    # binance_api_secret: str = Field(default="BINANCE_API_SECRET", env="BINANCE_API_SECRET")

    # Root path
    root_path: Path = Field(get_root_path(__file__, 1))

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
