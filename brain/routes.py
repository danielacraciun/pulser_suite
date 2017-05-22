import json
import os
import pickle

import requests
from flask import Flask, jsonify, session, request
from numpy import asarray

from constant import hr_ranges, user_data, current_model, trained_models_folder

app = Flask(__name__)

loaded_model = None

def check_hr_range(hr):
    actual_hr = hr[4]
    ranges = hr_ranges[int(hr[3])]
    for range in ranges.keys():
        if range[1] >= hr[2] >= range[0]:
            if ranges[range][1] >= actual_hr >= ranges[range][0]:
                return 1
    return 0


@app.route("/predict", methods=["POST", "GET"])
def get_rows():
    p = {"predict": "no", "result": -1}
    if request.data:
        data = request.data.decode('utf-8').replace('\\', '').replace('"{', '{').replace('}"', '}')
        data = json.loads(data)
        if data:
            row = [*user_data(), data["hr"]]  # send as 0 so it gets ignored by classifier

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

            if len(row) == 5:
                p = {"predict": "no", "hr_stat": check_hr_range(row), "hr": row[-1]}
            elif len(row) == 14:
                filename = "{}/{}".format(trained_models_folder, current_model)
                loaded_model = pickle.load(open(filename, 'rb'))
                predict_row = list(map(float, row))
                X = asarray(a=predict_row)
                res = loaded_model.predict(X)
                p = {"predict": "yes", "result": list(res)[0], "hr_stat": check_hr_range(row), "hr": row[-1]}
    return jsonify(p)


if __name__ == "__main__":
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host= '0.0.0.0', debug=True, port=9000)