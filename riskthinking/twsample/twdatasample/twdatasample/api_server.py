from flask import Flask, request, jsonify
import pandas as pd
from twdatasample.twutils import (
    getconfig,
    setuplogging,
    getsplitmodel,
)

# get config in global space
config = getconfig()
# setup logger
twlogger = setuplogging(config)

twlogger.info(
    "============================================================================="
)
twlogger.info("started model server")


# Load the trained model
twlogger.info("load trained model")
model = getsplitmodel(config)
twlogger.info("done loading")

# Create a Flask app
app = Flask(__name__)
twlogger.info(f"name {__name__}")


twlogger.info("start flask app")


# Define a route for model prediction
@app.route("/predict", methods=["POST"])
def predict():
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
    # Make predictions using the loaded model
    predictions = model.predict(dataDF)

    # Return the predictions as JSON response
    return jsonify({"predictions": predictions.tolist()})


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
