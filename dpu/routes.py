import json
import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)


def user_data():
    return [68, 174, 18, 1]


@app.route("/expose", methods=["POST", "GET"])
def exposer():
    # Actualization of hr resources
    requests.get("http://localhost:5000/api/hr/auth")
    # Fetch latest data
    r = requests.get("http://localhost:5000/api/forward")
    data = r.json()
    row = [*user_data()]
    if data:
        row.append(data["hr"]["value"])
        env = data["env"]
        env_values = {
            "accelerometer": [],
            "gyro": [],
            "magnetometer": []
        }
        if env:
            for env_data in env:
                env_values[env_data["type"]].append(env_data["X"])
                env_values[env_data["type"]].append(env_data["Y"])
                env_values[env_data["type"]].append(env_data["Z"])
            row.extend([*env_values["accelerometer"], *env_values["gyro"], *env_values["magnetometer"]])
    return jsonify(row)

if __name__ == "__main__":
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host= '0.0.0.0', debug=True, port=8000)