# root/src/runners/nautilus_node.py

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

import logging
import polars as pl

from nautilus_trader.adapters.binance import BINANCE_VENUE
from nautilus_trader.backtest.node import BacktestNode
from nautilus_trader.backtest.results import BacktestResult
from nautilus_trader.config import (
    BacktestDataConfig,
    BacktestEngineConfig,
    BacktestRunConfig,
    BacktestVenueConfig,
    ImportableStrategyConfig,
)
from nautilus_trader.model import Bar, BarType
from nautilus_trader.model.currencies import BTC, USDT
from nautilus_trader.model.identifiers import InstrumentId, Symbol, Venue
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.persistence.catalog import ParquetDataCatalog
from nautilus_trader.persistence.wranglers import BarDataWrangler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- Instrument + BarType -----------------------------------------------------

BTCUSD = CurrencyPair(
    instrument_id=InstrumentId(symbol=Symbol("BTCUSDT"), venue=Venue("BINANCE")),
    raw_symbol=Symbol("BTCUSDT"),
    base_currency=BTC,
    quote_currency=USDT,
    price_precision=2,
    size_precision=6,
    price_increment=Price(1e-02, precision=2),
    size_increment=Quantity(1e-06, precision=6),
    lot_size=None,
    max_quantity=Quantity(9000, precision=6),
    min_quantity=Quantity(1e-06, precision=6),
    max_notional=None,
    min_notional=Money(10.0, USDT),
    max_price=Price(1_000_000, precision=2),
    min_price=Price(0.01, precision=2),
    margin_init=Decimal(0),
    margin_maint=Decimal(0),
    maker_fee=Decimal("0.001"),
    taker_fee=Decimal("0.001"),
    ts_event=0,
    ts_init=0,
)

BTCUSDT_1H_LAST_EXT = BarType.from_str(f"{BTCUSD.id}-1-HOUR-LAST-EXTERNAL")


# --- Public API ---------------------------------------------------------------


def run_nautilus_simple_backtest(
    df: pl.DataFrame,
    catalog_path: str | Path,
    *,
    include_ema_example: bool = True,
    include_local_sma: bool = True,
    starting_balances: Optional[list[Money]] = None,
    trade_size: Decimal = Decimal("1"),
) -> Tuple[list[BacktestResult], Any]:
    """
    Build bars, write to Parquet catalog, run BacktestNode, and return (results, engine).

    Parameters
    ----------
    df : pl.DataFrame
        Polars OHLCV with columns: open_time, open, high, low, close, volume.
        open_time is the bar OPEN. Close is inferred as open_time + 1 hour.
    catalog_path : str | Path
        Filesystem path for ParquetDataCatalog.
    include_ema_example : bool
        Include built-in EMA cross example strategy.
    include_local_sma : bool
        Include local SMA cross strategy at `src/strategies/nautilus.py`.
    starting_balances : list[Money] | None
        Optional custom balances. Defaults to [1,000,000 USDT, 1 BTC].
    write_catalog_instrument : bool
        If True, write instrument to catalog.
    write_catalog_bars : bool
        If True, write bars to catalog.
    trade_size : Decimal
        Strategy trade size.

    Returns
    -------
    (results, engine)
        results: list[BacktestResult]
        engine: first BacktestEngine instance if available, else None.
    """
    catalog_path = str(Path(catalog_path))
    catalog = ParquetDataCatalog(catalog_path)
    logger.info("Catalog at %s", catalog_path)

    # Build bars and write to catalog
    bars = list(_bars_from_polars(df))
    logger.info("Prepared %d bars", len(bars))

    catalog.write_data([BTCUSD])
    logger.info("Wrote instrument to catalog")

    catalog.write_data(bars)
    logger.info("Wrote bars to catalog")

    # Data config
    data_config = BacktestDataConfig(
        catalog_path=catalog_path,
        data_cls=Bar,
        instrument_id=BTCUSD.id,
        bar_types=[BTCUSDT_1H_LAST_EXT],
    )

    # Venue config (spot)
    venue_config = BacktestVenueConfig(
        name=str(BINANCE_VENUE),
        oms_type="NETTING",
        account_type="CASH",
        base_currency=None,
        starting_balances=starting_balances
        or [Money(1_000_000.0, USDT), Money(1.0, BTC)],
    )

    # Strategies
    strategies = _build_strategies(
        include_ema_example=include_ema_example,
        include_local_sma=include_local_sma,
        trade_size=trade_size,
    )

    run_config = BacktestRunConfig(
        engine=BacktestEngineConfig(strategies=strategies),
        venues=[venue_config],
        data=[data_config],
    )

    node = BacktestNode(configs=[run_config])
    results: list[BacktestResult] = node.run()

    # Try to expose the first engine if available
    engine = getattr(node, "engines", None)
    engine = engine[0] if isinstance(engine, list) and engine else None

    return results, engine


# --- Helpers ------------------------------------------------------------------


def _bars_from_polars(df: pl.DataFrame) -> Iterable:
    """
    Convert a Polars OHLCV DataFrame to Nautilus bars with BarDataWrangler.

    Required columns:
      - open_time (ns, ms, s, or datetime). Represents bar open. Close = open_time + 1h.
      - open, high, low, close, volume

    Returns an iterable of Bar events for the configured BarType/instrument.
    """
    required = {"open_time", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # Ensure open_time is proper temporal type, then set bar close as timestamp
    if df.schema["open_time"] not in (pl.Datetime, pl.Date, pl.Time):
        df = df.with_columns(pl.col("open_time").cast(pl.Datetime, strict=False))

    df_pd = (
        df.with_columns((pl.col("open_time") + pl.duration(hours=1)).alias("timestamp"))
        .select(["timestamp", "open", "high", "low", "close", "volume"])
        .to_pandas()
    )
    df_pd = df_pd.set_index("timestamp")

    wrangler = BarDataWrangler(bar_type=BTCUSDT_1H_LAST_EXT, instrument=BTCUSD)
    return wrangler.process(df_pd)


def _build_strategies(
    include_ema_example: bool,
    include_local_sma: bool,
    trade_size: Decimal,
) -> list[ImportableStrategyConfig]:
    strategies: list[ImportableStrategyConfig] = []

    if include_ema_example:
        strategies.append(
            ImportableStrategyConfig(
                strategy_path="nautilus_trader.examples.strategies.ema_cross:EMACross",
                config_path="nautilus_trader.examples.strategies.ema_cross:EMACrossConfig",
                config={
                    "instrument_id": BTCUSD.id,
                    "bar_type": BTCUSDT_1H_LAST_EXT,
                    "fast_ema_period": 30,
                    "slow_ema_period": 100,
                    "trade_size": trade_size,
                },
            )
        )

    if include_local_sma:
        # Requires user-defined strategy at src/strategies/nautilus.py
        strategies.append(
            ImportableStrategyConfig(
                strategy_path="src.strategies.nautilus:SmaCrossNT",
                config_path="src.strategies.nautilus:SmaCrossConfig",
                config={
                    "instrument_id": BTCUSD.id,
                    "bar_type": BTCUSDT_1H_LAST_EXT,
                    "fast_sma_period": 30,
                    "slow_sma_period": 100,
                    "trade_size": trade_size,
                },
            )
        )

    if not strategies:
        raise ValueError("No strategies selected.")
    return strategies