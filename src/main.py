# src/main.py

from config.config import CONFIG
from data.data_pipeline import get_historical_data
from utils.utils import polars_to_pandas
from backtesting import Backtest
from strategies.backtesting_py import SmaCross_bt
import pandas as pd

def run_bt_sma_backtest(df_pl):

    # Convert to pandas DataFrame
    df_pd = polars_to_pandas(df_pl)

    #Create and run the backtest
    bt = Backtest(df_pd, SmaCross_bt, cash=1_000_000, commission=.002)
    stats = bt.run()
    print(stats)

    #plot the results
    #bt.plot()

def main():

    df = get_historical_data(download=False)
    run_bt_sma_backtest(df)

if __name__ == "__main__":
    main()
