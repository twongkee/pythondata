from flask import Flask, request, jsonify
import pandas as pd
from twdatasample.twutils import (
    getconfig,
    setuplogging,
    getsplitmodel,
)
from twdatasample import initial_setup, get_data, shrink_data, train_model


# get config in global space
config = getconfig()
# setup logger
twlogger = setuplogging(config)

twlogger.info(
    "============================================================================="
)
twlogger.info("started model server")

model = "unloaded"

# Create a Flask app
app = Flask(__name__)
twlogger.info(f"name {__name__}")


twlogger.info("start flask app")


# Define a route to initialize
@app.route("/initialize", methods=["POST"])
def initialize():
    rawdata = request.get_json()
    twlogger.info(f"initialize: {rawdata}")

    result = initial_setup.run()
    return jsonify({"initialize": result})


# Define a route to load data
@app.route("/get_data", methods=["POST"])
def get_data():
    rawdata = request.get_json()
    twlogger.info(f"get_data: {rawdata}")

    result = get_data.run()
    return jsonify({"get_data": result})


# Define a route to shrink data
@app.route("/shrink", methods=["POST"])
def shrink():
    rawdata = request.get_json()
    twlogger.info(f"shrink: {rawdata}")

    result = shrink_data.run()
    return jsonify({"shrink": result})


# Define a route to train_model
@app.route("/train", methods=["POST"])
def train():
    rawdata = request.get_json()
    twlogger.info(f"train: {rawdata}")

    result = train_model.run()
    return jsonify({"train": result})


# Define a route to load_model
@app.route("/load_model", methods=["POST"])
def load_model():
    rawdata = request.get_json()
    twlogger.info(f"load_model: {rawdata}")
    # Load the trained model
    twlogger.info("load trained model")
    global model
    model = getsplitmodel(config)
    twlogger.info("done loading")
    result = "model loaded"
    # result = train_model.run()
    return jsonify({"model_loaded": result})


# Define a route for model prediction
@app.route("/predict", methods=["POST"])
def predict():
    global model
    # Get the data from the request
    rawdata = request.get_json()
    twlogger.info(f"data : {rawdata}")

    # Preprocess the data
    data = {
        "vol_moving_avg": [rawdata["vol_moving_avg"]],
        "adj_close_rolling_med": [rawdata["adj_close_rolling_med"]],
    }
    dataDF = pd.DataFrame.from_dict(data)

    twlogger.info("make predictions")
    if model == "unloaded":
        twlogger.info("model was unloaded")
        model = getsplitmodel(config)
    # Make predictions using the loaded model
    predictions = model.predict(dataDF)

    # Return the predictions as JSON response
    return jsonify({"predictions": predictions.tolist()})


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
