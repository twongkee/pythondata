import requests
import json

# Define the server URL
server_url = "http://localhost:5000/predict"

# Define the input data for prediction
data = {"vol_moving_avg": 12345, "adj_close_rolling_med": 25}

# Send a POST request to the server with the input data
response = requests.post(server_url, json=data)

print(response)
# Parse the JSON response
predictions = json.loads(response.text)["predictions"]

# Print the predictions
print(predictions)
