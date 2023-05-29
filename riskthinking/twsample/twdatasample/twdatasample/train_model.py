#!/usr/bin/env python
# coding: utf-8

# load parquet data
# some data transformation
# train model
# initial test
# persist model

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from twdatasample.twutils import (
    getconfig,
    setuplogging,
    splitjobdump,
    getcleandata,
)

config = getconfig()

mylogger = setuplogging(config)

mylogger.info(
    "============================================================================="
)
mylogger.info("started train model")

def run():
    data = getcleandata(config)

    mylogger.info("got cleaned data")
    # Select features and target
    features = ["vol_moving_avg", "adj_close_rolling_med"]
    target = "Volume"


    X = data[features]
    y = data[target]
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    estimators = config["model"]["estimators"]
    random_state = config["model"]["random_state"]
    n_jobs = config["model"]["n_jobs"]
    # Create a RandomForestRegressor model
    model = RandomForestRegressor(
        n_estimators=estimators, random_state=random_state, n_jobs=n_jobs, verbose=1
    )

    mylogger.info("start training")
    try:
        # Train the model
        model.fit(X_train, y_train)

    except Exception as e:
        mylogger.error(f"error {e}")

    mylogger.info("done trainig")

    model_dir = config["data"]["modeldir"]
    compression = config["data"]["compression"]
    compression_level = config["data"]["compression_level"]

    mylogger.info("start dump")
    splitjobdump(model, config)
    mylogger.info("dump complete")

    mylogger.info("make test predictions")
    # Make predictions on test data
    y_pred = model.predict(X_test)

    # Calculate the Mean Absolute Error and Mean Squared Error
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    mylogger.info(f"calculated errors {mae} , {mse}")
    mylogger.info("done train model")
    mylogger.info(
        "============================================================================="
    )

if __name__ == "__main__":
    run()