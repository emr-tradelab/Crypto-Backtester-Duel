# Notebook Insights

## 01_backtesting-py_simple.ipynb
- **Goal:** Evaluate a long-only SMA crossover strategy on BTCUSDT hourly data with the `backtesting.py` framework.
- **Data preparation:** Retrieves candles through `src.data.data_pipeline.get_historical_data`, then converts the Polars DataFrame to pandas for compatibility with `Backtest`.
- **Strategy logic:** Implements `SmaCross_bt`, which tracks short/long simple moving averages, buys on upward crossovers, and exits on downward crossovers.
- **Backtest run:** Executes `Backtest` with \$1M starting cash, 0.2% commission, and exclusive orders; prints the resulting performance statistics and generates the HTML equity plot.
- **Optimization experiments:** Runs a 300-trial Optuna study optimizing both return and Sharpe ratio (multi-objective) followed by a single-objective variant that combines the same metrics, then re-runs the backtest with the chosen parameters (`n_short=47`, `n_long=67`).

## 02_nautilus_simple_low-level.ipynb
- **Goal:** Reproduce the SMA crossover strategy using NautilusTrader's low-level backtesting engine APIs.
- **Data preparation:** Loads the BTCUSDT parquet file with Polars, adjusts timestamps to hour-close boundaries, reorders columns, and converts to pandas to satisfy the wrangler's expectations.
- **Catalog & bars:** Builds a `ParquetDataCatalog`, instantiates the Binance BTCUSDT instrument from the test kit, derives a matching `BarType`, and processes the pandas frame into Nautilus `BarData` via `BarDataWrangler`.
- **Engine configuration:** Creates a `BacktestEngine` with logging enabled, registers the Binance venue with NETTING/CASH settings, seeds balances in USDT and BTC, then attaches the instrument and prepared bars.
- **Strategy run:** Configures `SmaCrossNT` (fast=30, slow=100, trade size 1 BTC), adds it to the engine, executes the simulation, and inspects generated account, order, and position reports before resetting/disposing the engine.

## 03_nautilus_simple_high-level.ipynb
- **Goal:** Exercise the higher-level NautilusTrader `BacktestNode` workflow for the same SMA crossover idea.
- **Data preparation:** Mirrors the parquet ingestion from the low-level notebook, writes both the BTCUSDT instrument definition and wrangled bars into a local `ParquetDataCatalog`, and validates catalog contents (instruments, bar types, venues).
- **Backtest configuration:** Defines `BacktestDataConfig` pointing at the cataloged BTCUSDT hourly bars, and `BacktestVenueConfig` mirroring the Binance NETTING/CASH account with seeded USDT/BTC balances.
- **Strategy wiring:** Uses `ImportableStrategyConfig` to load `SmaCrossNT`/`SmaCrossConfig` from `src.strategies.nautilus`, keeping the 30/100 SMA windows and a 0.1 BTC trade size.
- **Execution & reporting:** Bundles configs into `BacktestRunConfig`, runs them through `BacktestNode`, then retrieves the underlying engine to produce account, order, and position reports for review.
