# AGENTS.md

## Scope and Goals of this codebase/project

* Python project to compare two backtesting frameworks:
  * **backtesting.py**
  * **nautilustrader**
* Run identical simple strategies on both.
* Measure performance, output parity, and runtime.
* If results diverge, document root causes and justify differences.
* Data: BTCUSDT 1h bars. Primary source via Binance (CCXT was tested but slower).
* Workflow final target (invoked from `main.py`):

  1. Load or download data
  2. Run backtests on both frameworks
  3. Produce comparisons: strategy metrics, runtime, cpu use, etc.

Dependencies are managed with **uv**. See `pyproject.toml` for versions.

## Coding Standards

### Language and typing

* Python ≥ version in `.python-version`.
* Full **type hints**. No `Any` unless unavoidable.
* Strict mypy/pyright settings recommended. Treat warnings as errors.

### Docstrings and comments

* **Google style docstrings** for all public modules, classes, functions: Include `Args`, `Returns`, `Raises`, and `Examples` when relevant.
* Document non-obvious complexity with brief inline comments, not prose.

### Structure and imports

* Keep framework-specific code isolated under `src/strategies/`.
* Shared utilities in `src/utils/`. No framework imports inside utils.
* Absolute imports within `src`. Avoid circular deps.

### Data and time

* Mandatory Polars for dataframe handling.
  * Docs: Polars evolves quickly — always consult the latest Polars documentation for complex operations.
* All timestamps in **UTC**. Validate timezone on load.
* Enforce schema for OHLCV: `timestamp, open, high, low, close, volume`.

### Determinism and randomness

* Fix random seeds for any stochastic component.

### Linting and formatting

* **Ruff** for lint + format. Target PEP8 plus:

  * Max line length 100.
  * F-strings preferred. No string `.format`.
  * No wildcard imports.
* Keep notebooks free of heavy logic. Move logic to `src/` and import.