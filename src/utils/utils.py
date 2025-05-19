
import pandas as pd
import polars as pl


def polars_to_pandas(df_pl: pl.DataFrame) -> pd.DataFrame:
    """
    Convert a Polars DataFrame to a pandas DataFrame
    and rename columns as needed for backtesting.py
    """

    df_pd = df_pl.rename(
        {
            "open_time": "timestamp",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    ).to_pandas()

    # Also ensure the index is datetime-based if needed:
    if "timestamp" in df_pd.columns:
        df_pd["timestamp"] = pd.to_datetime(df_pd["timestamp"])
        df_pd.set_index("timestamp", inplace=True)

    return df_pd
