import os
import pickle

import requests
from flask import Flask, jsonify, session
from numpy import asarray

from constant import hr_ranges

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
    r = requests.get("http://localhost:8000/expose")
    data = r.json()
    print(data)
    if len(data) == 5:
        p = {"predict": "no", "result": check_hr_range(data), "hr": data}
    elif len(data) == 14:
        filename = "model_0445.sav"
        loaded_model = pickle.load(open(filename, 'rb'))
        row = list(map(float, data))
        X = asarray(a=row)
        res = loaded_model.predict(X)
        p = {"predict": "yes", "result": list(res)[0]}
    return jsonify(p)


if __name__ == "__main__":
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host= '0.0.0.0', debug=True, port=9000)