# Project Summary

This project demonstrates a Proof of Concept (PoC) for crypto trading strategy backtesting using two libraries:
- [nautilustrader](https://nautilustrader.io): Known for high-performance, low-latency trading simulations.
- [backtesting.py](https://kernc.github.io/backtesting.py/): Offers simpler setup and built-in visualization for strategy evaluation.

### Conclusions

The two frameworks were in the end run for comparison with a simple dummy strategy (30/100 slow/fast SMA) and—despite the strategies being essentially the same—produced markedly different results. The leading hypothesis is that differences in order sizing (minimum trade size / lot rounding), execution and commission/fee modelling between backtesting.py and NautilusTrader account for most of the divergence. A detailed root-cause analysis is outside the scope of this repository and will be pursued in future investigations.

### Features

- **Binance API** integration for historical data retrieval (API keys optional for the sample scripts).
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

> **Note:** All historical market-data endpoints used in this project are public. Binance API keys can still be supplied via the
> `BINANCE_API_KEY` and `BINANCE_API_SECRET` environment variables (or a `.env` file) if you have them, but they are optional.

### Results

#### Backtesting.py

```plain
Start                     2024-09-24 16:00:00                                                                                             
End                       2025-09-24 15:00:00
Duration                    364 days 23:00:00
Exposure Time [%]                    55.73059
Equity Final [$]                1094161.98954
Equity Peak [$]                 1535359.05996
Commissions [$]                  244949.18046
Return [%]                             9.4162
Buy & Hold Return [%]                72.45817
Return (Ann.) [%]                      9.3893
Volatility (Ann.) [%]                36.43405
CAGR [%]                              9.41732
Sharpe Ratio                          0.25771
Sortino Ratio                         0.46411
Calmar Ratio                          0.26886
Alpha [%]                           -27.91721
Beta                                  0.51524
Max. Drawdown [%]                   -34.92262
Avg. Drawdown [%]                    -2.13122
Max. Drawdown Duration      281 days 01:00:00
Avg. Drawdown Duration        7 days 05:00:00
# Trades                                   53
Win Rate [%]                         33.96226
Best Trade [%]                        35.6561
Worst Trade [%]                      -5.53797
Avg. Trade [%]                        0.17558
Max. Trade Duration          18 days 19:00:00
Avg. Trade Duration           3 days 20:00:00
Profit Factor                          1.2417
Expectancy [%]                         0.3247
SQN                                   0.21117
Kelly Criterion                       0.03457
```

#### NautilusTrader - Long only manual strategy

```plain
2025-10-16T15:14:29.652757000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.652759000Z [INFO] BACKTESTER-001.BacktestEngine:  BACKTEST POST-RUN
2025-10-16T15:14:29.652759001Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.652759002Z [INFO] BACKTESTER-001.BacktestEngine: Run config ID:  f98f7b8bfbe8c891b7101d9975ba62931839bbde71e96e3093bbe7bd20fc5c4a
2025-10-16T15:14:29.652760000Z [INFO] BACKTESTER-001.BacktestEngine: Run ID:         6aebcafb-30d5-47eb-a7ed-4c84bc8e157b
2025-10-16T15:14:29.652766000Z [INFO] BACKTESTER-001.BacktestEngine: Run started:    2025-10-16T15:14:29.466128000Z
2025-10-16T15:14:29.652767000Z [INFO] BACKTESTER-001.BacktestEngine: Run finished:   2025-10-16T15:14:29.652733000Z
2025-10-16T15:14:29.652782000Z [INFO] BACKTESTER-001.BacktestEngine: Elapsed time:   0 days 00:00:00.186605
2025-10-16T15:14:29.652784000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest start: 2024-09-24T17:00:00.000000000Z
2025-10-16T15:14:29.652785000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest end:   2025-09-24T16:00:00.000000000Z
2025-10-16T15:14:29.652789000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest range: 364 days 23:00:00
2025-10-16T15:14:29.652791000Z [INFO] BACKTESTER-001.BacktestEngine: Iterations: 8_760
2025-10-16T15:14:29.652793000Z [INFO] BACKTESTER-001.BacktestEngine: Total events: 216
2025-10-16T15:14:29.652849000Z [INFO] BACKTESTER-001.BacktestEngine: Total orders: 108
2025-10-16T15:14:29.653598000Z [INFO] BACKTESTER-001.BacktestEngine: Total positions: 54
2025-10-16T15:14:29.653602000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.653603000Z [INFO] BACKTESTER-001.BacktestEngine:  SimulatedVenue BINANCE
2025-10-16T15:14:29.653603001Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.653605000Z [INFO] BACKTESTER-001.BacktestEngine: CashAccount(id=BINANCE-001, type=CASH, base=None)
2025-10-16T15:14:29.653606000Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.653606001Z [INFO] BACKTESTER-001.BacktestEngine: Balances starting:
2025-10-16T15:14:29.653610000Z [INFO] BACKTESTER-001.BacktestEngine: 1_000_000.00000000 USDT
2025-10-16T15:14:29.653612000Z [INFO] BACKTESTER-001.BacktestEngine: 1.00000000 BTC
2025-10-16T15:14:29.653612001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.653612002Z [INFO] BACKTESTER-001.BacktestEngine: Balances ending:
2025-10-16T15:14:29.653614000Z [INFO] BACKTESTER-001.BacktestEngine: 1_010_263.93518000 USDT
2025-10-16T15:14:29.653615000Z [INFO] BACKTESTER-001.BacktestEngine: 1.00000000 BTC
2025-10-16T15:14:29.653615001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.653616000Z [INFO] BACKTESTER-001.BacktestEngine: Commissions:
2025-10-16T15:14:29.653619000Z [INFO] BACKTESTER-001.BacktestEngine: -10_609.78482000 USDT
2025-10-16T15:14:29.653619001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.653619002Z [INFO] BACKTESTER-001.BacktestEngine: Unrealized PnLs (included in totals):
2025-10-16T15:14:29.653630000Z [INFO] BACKTESTER-001.BacktestEngine: None
2025-10-16T15:14:29.653632000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.653632001Z [INFO] BACKTESTER-001.BacktestEngine:  PORTFOLIO PERFORMANCE
2025-10-16T15:14:29.653632002Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:14:29.664661000Z [INFO] BACKTESTER-001.BacktestEngine:  PnL Statistics (BTC)
2025-10-16T15:14:29.664664000Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.664704000Z [INFO] BACKTESTER-001.BacktestEngine: PnL (total):                    0.0
2025-10-16T15:14:29.664706000Z [INFO] BACKTESTER-001.BacktestEngine: PnL% (total):                   0.0
2025-10-16T15:14:29.664707000Z [INFO] BACKTESTER-001.BacktestEngine: Max Winner:                     0.0
2025-10-16T15:14:29.664707001Z [INFO] BACKTESTER-001.BacktestEngine: Avg Winner:                     0.0
2025-10-16T15:14:29.664707002Z [INFO] BACKTESTER-001.BacktestEngine: Min Winner:                     0.0
2025-10-16T15:14:29.664707003Z [INFO] BACKTESTER-001.BacktestEngine: Min Loser:                      0.0
2025-10-16T15:14:29.664707004Z [INFO] BACKTESTER-001.BacktestEngine: Avg Loser:                      0.0
2025-10-16T15:14:29.664707005Z [INFO] BACKTESTER-001.BacktestEngine: Max Loser:                      0.0
2025-10-16T15:14:29.664708000Z [INFO] BACKTESTER-001.BacktestEngine: Expectancy:                     0.0
2025-10-16T15:14:29.664708001Z [INFO] BACKTESTER-001.BacktestEngine: Win Rate:                       0.0
2025-10-16T15:14:29.664708002Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.664709000Z [INFO] BACKTESTER-001.BacktestEngine:  PnL Statistics (USDT)
2025-10-16T15:14:29.664709001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.664803000Z [INFO] BACKTESTER-001.BacktestEngine: PnL (total):                    10_263.93518
2025-10-16T15:14:29.664805000Z [INFO] BACKTESTER-001.BacktestEngine: PnL% (total):                   1.0263935180000028
2025-10-16T15:14:29.664805001Z [INFO] BACKTESTER-001.BacktestEngine: Max Winner:                     25_529.7247
2025-10-16T15:14:29.664805002Z [INFO] BACKTESTER-001.BacktestEngine: Avg Winner:                     3_880.3575769999998
2025-10-16T15:14:29.664805003Z [INFO] BACKTESTER-001.BacktestEngine: Min Winner:                     104.7831
2025-10-16T15:14:29.664805004Z [INFO] BACKTESTER-001.BacktestEngine: Min Loser:                      -61.10207
2025-10-16T15:14:29.664806000Z [INFO] BACKTESTER-001.BacktestEngine: Avg Loser:                      -1_980.6828341176467
2025-10-16T15:14:29.664806001Z [INFO] BACKTESTER-001.BacktestEngine: Max Loser:                      -5_656.2100199999995
2025-10-16T15:14:29.664806002Z [INFO] BACKTESTER-001.BacktestEngine: Expectancy:                     190.07287370370364
2025-10-16T15:14:29.664806003Z [INFO] BACKTESTER-001.BacktestEngine: Win Rate:                       0.37037037037037035
2025-10-16T15:14:29.664806004Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.664807000Z [INFO] BACKTESTER-001.BacktestEngine:  Returns Statistics
2025-10-16T15:14:29.664807001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.667086000Z [INFO] BACKTESTER-001.BacktestEngine: Returns Volatility (252 days):  0.3637645599673481
2025-10-16T15:14:29.667088000Z [INFO] BACKTESTER-001.BacktestEngine: Average (Return):               0.0067290562657433
2025-10-16T15:14:29.667088001Z [INFO] BACKTESTER-001.BacktestEngine: Average Loss (Return):          -0.019439683535760432
2025-10-16T15:14:29.667088002Z [INFO] BACKTESTER-001.BacktestEngine: Average Win (Return):           0.041999966432987444
2025-10-16T15:14:29.667088003Z [INFO] BACKTESTER-001.BacktestEngine: Sharpe Ratio (252 days):        0.7070955059414841
2025-10-16T15:14:29.667089000Z [INFO] BACKTESTER-001.BacktestEngine: Sortino Ratio (252 days):       2.305032731251375
2025-10-16T15:14:29.667089001Z [INFO] BACKTESTER-001.BacktestEngine: Profit Factor:                  1.6029718467741503
2025-10-16T15:14:29.667089002Z [INFO] BACKTESTER-001.BacktestEngine: Risk Return Ratio:              0.11410057205267639
2025-10-16T15:14:29.667090000Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.667090001Z [INFO] BACKTESTER-001.BacktestEngine:  General Statistics
2025-10-16T15:14:29.667090002Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:14:29.667105000Z [INFO] BACKTESTER-001.BacktestEngine: Long Ratio:                     1.00
2025-10-16T15:14:29.667105001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
```

#### NautilusTrader - Long Short example from nautilus_trader

```plain
2025-10-16T15:19:19.519140000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.519141000Z [INFO] BACKTESTER-001.BacktestEngine:  BACKTEST POST-RUN
2025-10-16T15:19:19.519141001Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.519142000Z [INFO] BACKTESTER-001.BacktestEngine: Run config ID:  f67b630c5e962cf17112aba64ec7a78b3603e302328fe16ad2cd9f094626973c
2025-10-16T15:19:19.519143000Z [INFO] BACKTESTER-001.BacktestEngine: Run ID:         39b729bf-259b-458f-9f62-d7df8626be00
2025-10-16T15:19:19.519147000Z [INFO] BACKTESTER-001.BacktestEngine: Run started:    2025-10-16T15:19:19.354411000Z
2025-10-16T15:19:19.519148000Z [INFO] BACKTESTER-001.BacktestEngine: Run finished:   2025-10-16T15:19:19.519120000Z
2025-10-16T15:19:19.519161000Z [INFO] BACKTESTER-001.BacktestEngine: Elapsed time:   0 days 00:00:00.164709
2025-10-16T15:19:19.519162000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest start: 2024-09-24T17:00:00.000000000Z
2025-10-16T15:19:19.519163000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest end:   2025-09-24T16:00:00.000000000Z
2025-10-16T15:19:19.519165000Z [INFO] BACKTESTER-001.BacktestEngine: Backtest range: 364 days 23:00:00
2025-10-16T15:19:19.519167000Z [INFO] BACKTESTER-001.BacktestEngine: Iterations: 8_760
2025-10-16T15:19:19.519168000Z [INFO] BACKTESTER-001.BacktestEngine: Total events: 392
2025-10-16T15:19:19.519250000Z [INFO] BACKTESTER-001.BacktestEngine: Total orders: 196
2025-10-16T15:19:19.521972000Z [INFO] BACKTESTER-001.BacktestEngine: Total positions: 98
2025-10-16T15:19:19.521980000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.521982000Z [INFO] BACKTESTER-001.BacktestEngine:  SimulatedVenue BINANCE
2025-10-16T15:19:19.521983000Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.521986000Z [INFO] BACKTESTER-001.BacktestEngine: CashAccount(id=BINANCE-001, type=CASH, base=None)
2025-10-16T15:19:19.521986001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.521987000Z [INFO] BACKTESTER-001.BacktestEngine: Balances starting:
2025-10-16T15:19:19.521998000Z [INFO] BACKTESTER-001.BacktestEngine: 1_000_000.00000000 USDT
2025-10-16T15:19:19.522000000Z [INFO] BACKTESTER-001.BacktestEngine: 1.00000000 BTC
2025-10-16T15:19:19.522000001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.522000002Z [INFO] BACKTESTER-001.BacktestEngine: Balances ending:
2025-10-16T15:19:19.522003000Z [INFO] BACKTESTER-001.BacktestEngine: 959_854.25307000 USDT
2025-10-16T15:19:19.522004000Z [INFO] BACKTESTER-001.BacktestEngine: 1.00000000 BTC
2025-10-16T15:19:19.522004001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.522005000Z [INFO] BACKTESTER-001.BacktestEngine: Commissions:
2025-10-16T15:19:19.522009000Z [INFO] BACKTESTER-001.BacktestEngine: -19_082.77693000 USDT
2025-10-16T15:19:19.522009001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.522009002Z [INFO] BACKTESTER-001.BacktestEngine: Unrealized PnLs (included in totals):
2025-10-16T15:19:19.522029000Z [INFO] BACKTESTER-001.BacktestEngine: None
2025-10-16T15:19:19.522029001Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.522030000Z [INFO] BACKTESTER-001.BacktestEngine:  PORTFOLIO PERFORMANCE
2025-10-16T15:19:19.522030001Z [INFO] BACKTESTER-001.BacktestEngine: =================================================================
2025-10-16T15:19:19.548922000Z [INFO] BACKTESTER-001.BacktestEngine:  PnL Statistics (BTC)
2025-10-16T15:19:19.548924000Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.548959000Z [INFO] BACKTESTER-001.BacktestEngine: PnL (total):                    0.0
2025-10-16T15:19:19.548960000Z [INFO] BACKTESTER-001.BacktestEngine: PnL% (total):                   0.0
2025-10-16T15:19:19.548960001Z [INFO] BACKTESTER-001.BacktestEngine: Max Winner:                     0.0
2025-10-16T15:19:19.548960002Z [INFO] BACKTESTER-001.BacktestEngine: Avg Winner:                     0.0
2025-10-16T15:19:19.548960003Z [INFO] BACKTESTER-001.BacktestEngine: Min Winner:                     0.0
2025-10-16T15:19:19.548960004Z [INFO] BACKTESTER-001.BacktestEngine: Min Loser:                      0.0
2025-10-16T15:19:19.548960005Z [INFO] BACKTESTER-001.BacktestEngine: Avg Loser:                      0.0
2025-10-16T15:19:19.548961000Z [INFO] BACKTESTER-001.BacktestEngine: Max Loser:                      0.0
2025-10-16T15:19:19.548961001Z [INFO] BACKTESTER-001.BacktestEngine: Expectancy:                     0.0
2025-10-16T15:19:19.548961002Z [INFO] BACKTESTER-001.BacktestEngine: Win Rate:                       0.0
2025-10-16T15:19:19.548961003Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.548962000Z [INFO] BACKTESTER-001.BacktestEngine:  PnL Statistics (USDT)
2025-10-16T15:19:19.548962001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.549055000Z [INFO] BACKTESTER-001.BacktestEngine: PnL (total):                    -40_145.74693
2025-10-16T15:19:19.549055001Z [INFO] BACKTESTER-001.BacktestEngine: PnL% (total):                   -4.01457469299999
2025-10-16T15:19:19.549056000Z [INFO] BACKTESTER-001.BacktestEngine: Max Winner:                     23_407.67448
2025-10-16T15:19:19.549056001Z [INFO] BACKTESTER-001.BacktestEngine: Avg Winner:                     3_528.1992518518523
2025-10-16T15:19:19.549056002Z [INFO] BACKTESTER-001.BacktestEngine: Min Winner:                     32.14772
2025-10-16T15:19:19.549056003Z [INFO] BACKTESTER-001.BacktestEngine: Min Loser:                      -83.15055
2025-10-16T15:19:19.549056004Z [INFO] BACKTESTER-001.BacktestEngine: Avg Loser:                      -1_907.1426300000003
2025-10-16T15:19:19.549057000Z [INFO] BACKTESTER-001.BacktestEngine: Max Loser:                      -10_854.3107
2025-10-16T15:19:19.549057001Z [INFO] BACKTESTER-001.BacktestEngine: Expectancy:                     -409.65047887755134
2025-10-16T15:19:19.549057002Z [INFO] BACKTESTER-001.BacktestEngine: Win Rate:                       0.2755102040816326
2025-10-16T15:19:19.549057003Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.549057004Z [INFO] BACKTESTER-001.BacktestEngine:  Returns Statistics
2025-10-16T15:19:19.549058000Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.551356000Z [INFO] BACKTESTER-001.BacktestEngine: Returns Volatility (252 days):  0.3854773022353435
2025-10-16T15:19:19.551357000Z [INFO] BACKTESTER-001.BacktestEngine: Average (Return):               -0.001127899744995034
2025-10-16T15:19:19.551357001Z [INFO] BACKTESTER-001.BacktestEngine: Average Loss (Return):          -0.01834209889842878
2025-10-16T15:19:19.551357002Z [INFO] BACKTESTER-001.BacktestEngine: Average Win (Return):           0.03983002237869215
2025-10-16T15:19:19.551357003Z [INFO] BACKTESTER-001.BacktestEngine: Sharpe Ratio (252 days):        -0.20072238250598903
2025-10-16T15:19:19.551358000Z [INFO] BACKTESTER-001.BacktestEngine: Sortino Ratio (252 days):       -0.42377566817864254
2025-10-16T15:19:19.551358001Z [INFO] BACKTESTER-001.BacktestEngine: Profit Factor:                  0.9126629632613914
2025-10-16T15:19:19.551358002Z [INFO] BACKTESTER-001.BacktestEngine: Risk Return Ratio:              -0.024391672359192103
2025-10-16T15:19:19.551358003Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.551359000Z [INFO] BACKTESTER-001.BacktestEngine:  General Statistics
2025-10-16T15:19:19.551359001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
2025-10-16T15:19:19.551373000Z [INFO] BACKTESTER-001.BacktestEngine: Long Ratio:                     0.50
2025-10-16T15:19:19.551373001Z [INFO] BACKTESTER-001.BacktestEngine: -----------------------------------------------------------------
```