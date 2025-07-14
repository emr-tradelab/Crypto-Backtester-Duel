# Project Summary

This project demonstrates a Proof of Concept (PoC) for crypto trading strategy backtesting using two libraries:
- [nautilustrader](https://nautilustrader.io): Known for high-performance, low-latency trading simulations.
- [backtesting.py](https://kernc.github.io/backtesting.py/): Offers simpler setup and built-in visualization for strategy evaluation.

### Features

- **Binance API** integration for historical data retrieval.
- A **simple PoC trading strategy** to showcase both frameworks.
- Comparative tests to highlight performance and visualization differences.
- Clear modular structure for future scaling and Docker integration.

### Data Download Approach

I tested two methods for retrieving historical OHLC data from Binance:
1. **CCXT-based approach**
2. **Direct Binance API** (via [python-binance](https://github.com/sammchardy/python-binance))

In quick comparisons over a 3-month historical range at 1-hour intervals, the direct Binance approach fetched data more than **3x faster** than CCXT (around 1.13 seconds vs. 4.33 seconds).

For **faster iteration** in repeated backtests, we will:
- Use the **Direct Binance API** for data download.
- Save fetched data to a **temporary Parquet file**, so we can skip re-fetching from the exchange on subsequent runs.
