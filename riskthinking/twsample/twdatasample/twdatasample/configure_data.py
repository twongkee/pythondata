import pandas as pd
from twdatasample.twutils import getconfig, setuplogging

config = getconfig()

mylogger = setuplogging(config)

mylogger.info(
    "============================================================================="
)
mylogger.info("started configure data")

def run():
    # code specific to this dataset
    # customize for different datasets
    rootdir = config["data"]["kaggle"]
    meta = rootdir + "/symbols_valid_meta.csv"
    # read raw local csv data
    df_meta = pd.read_csv(meta)
    # choice:
    # put each symbol into separate parquet file to match input csv structure
    # could also separate by year-month-day (putting all symbols into one file per day)
    #  which may be useful if is an updating time series
    df_all = list()
    for index, row in df_meta.iterrows():
        symbol = row["NASDAQ Symbol"]
        etf = row["ETF"]
        # print(symbol)
        try:
            if etf == "Y":
                fname = f"{rootdir}/etfs/{symbol}.csv"
            else:
                fname = f"{rootdir}/stocks/{symbol}.csv"

            df_security = pd.read_csv(fname)
            df_security["NASDAQ Symbol"] = symbol
            df_all.append(df_security)
        except Exception as e:
            print(f"bad symbol {symbol}", e)
    # remove extra columns to save space
    df_meta_min = df_meta.drop(
        columns=[
            "Nasdaq Traded",
            "Listing Exchange",
            "ETF",
            "Market Category",
            "Round Lot Size",
            "Test Issue",
            "Financial Status",
            "CQS Symbol",
            "NextShares",
        ]
    )
    joined_df_list = list()
    for df in df_all:
        df_joined = df.join(
            df_meta_min.set_index("NASDAQ Symbol"), on="NASDAQ Symbol", how="left"
        )
        joined_df_list.append(df_joined)
    # export
    parquetdir = config["data"]["parquet"]
    featuredir = config["data"]["featuredir"]
    for df in joined_df_list:
        fname = df["NASDAQ Symbol"].iloc[0]
        # using basic pandas calculations
        # customize for different calcuations here
        df["vol_moving_avg"] = df["Volume"].rolling(30).mean()
        df["adj_close_rolling_med"] = df["Adj Close"].rolling(30).median()
        # write out basic data
        df.to_parquet(f"{parquetdir}/{fname}.parquet.gzip", compression="gzip")
        # smaller feature data set without extra data
        df_features = df.drop(
            columns=["Open", "High", "Low", "Close", "Adj Close", "Security Name", "Symbol"]
        )
        df_features.to_parquet(f"{featuredir}/{fname}.parquet.gzip", compression="gzip")

    mylogger.info("completed configure data")

if __name__ == "__main__":
    run()