#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import joblib
from datetime import datetime
import yaml
import logging
from twdatasample.twutils import (
    getconfig,
    setuplogging,
    getsplitmodel,
    getcleandata,
)

# get config in global space
config = getconfig()

twlogger = setuplogging(config)

twlogger.info(
    "============================================================================="
)
twlogger.info("started run model")


data = getcleandata(config)
twlogger.info("cleaned data loaded")

# Select features and target
features = ["vol_moving_avg", "adj_close_rolling_med"]
target = "Volume"
X = data[features]
y = data[target]
# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


twlogger.info("load trained model")
model = getsplitmodel(config)
twlogger.info("done loading")

twlogger.info("make predictions")
# Make predictions on test data
y_pred = model.predict(X_test)

# Calculate the Mean Absolute Error and Mean Squared Error
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("errors", mae, mse, flush=True)
twlogger.info(f"calculated errors {mae} , {mse}")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("joblib done:", current_time, flush=True)
print("end job train run")

twlogger.info("done run model")
twlogger.info(
    "============================================================================="
)
