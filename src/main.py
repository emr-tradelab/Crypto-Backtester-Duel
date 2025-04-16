# src/main.py
import time
from datetime import datetime, timedelta, timezone

from config.config import CONFIG
from data.data_pipeline import binance_direct_fetch, save_tmp_data, load_tmp_data

def get_historical_data(download=False):

    if download:
        print("\nStarting Direct Binance download ...")
        df_direct = binance_direct_fetch()
        print(f"Direct Binance result: {df_direct.head()}")
        print(f"Direct Binance result shape: {df_direct.shape}")
        save_tmp_data(df_direct, CONFIG.DATA_TMP_PATH)
    else:
        print("\nLoading Direct Binance data from tmp file ...")
        df_direct = load_tmp_data(CONFIG.DATA_TMP_PATH)
        print(f"Direct Binance result: {df_direct.head()}")
        print(f"Direct Binance result shape: {df_direct.shape}")
    
    return df_direct

def main():

    df = get_historical_data(download=False)

if __name__ == "__main__":
    main()
