import json
import os

import requests
from flask import Flask, jsonify, request

from utils import user_data

app = Flask(__name__)


@app.route("/expose", methods=["POST", "GET"])
def exposer():
    # import pudb; pu.db
    row = {}
    if request.data:
        data = request.data.decode('utf-8').replace('\\', '').replace('"{', '{').replace('}"', '}')
        data = json.loads(data)
        row = [*user_data()]
        if data:
            row.append(data["hr"])
            env = data["env"]
            env_values = {
                "accelerometer": [],
                "gyro": [],
                "magnetometer": []
            }
            if env:
                for env_data in env:
                    env_values[env_data["type"]].append(env_data["x"])
                    env_values[env_data["type"]].append(env_data["y"])
                    env_values[env_data["type"]].append(env_data["z"])
                row.extend([*env_values["accelerometer"], *env_values["gyro"], *env_values["magnetometer"]])
    r = requests.post("http://localhost:9000/predict", json=row)
    return jsonify(r.json())

if __name__ == "__main__":
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host= '0.0.0.0', debug=True, port=8000)