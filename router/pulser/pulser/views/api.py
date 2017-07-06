# -*- coding: utf-8 -*-
import json
from base64 import standard_b64encode

import dataset
from datetime import datetime, timedelta

import requests
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app, session, jsonify, Response)
from flask_login import login_required
from requests_oauthlib import OAuth2Session

from ..models.user import CareReceiver
from ..constants import authorization_base_url, FITBIT_URL, hr_mapper, activity_level_mapper
from ..models.env_data import FallEvent, ActivityLevel, HeartLevel, MovementSensor, HeartRateSensor, HeartData
from ..utils import insert_env_data, insert_hr_data, latest_hr, find_env_data, latest_env, group_env, find_hr_data

blueprint = Blueprint("api", __name__, url_prefix='/api',
                      static_folder="../static")

@blueprint.route("/hr/auth", methods=["POST", "GET"])
def auth():
    """ Step 1: Authorization for data fetching from FitBit
    """
    client_data = HeartRateSensor.query.first()
    client_id, client_secret = client_data.client_id, client_data.client_secret
    oauth_session = OAuth2Session(client_id, scope=['heartrate'])
    authorization_url, state = oauth_session.authorization_url(authorization_base_url)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@blueprint.route("/hr/fetch", methods=["GET", "POST"])
def hr():
    """Step 3: Fetching a protected resource using an OAuth 2 token. (in this case the intraday heartrate)
    struct:
    {
    "external": 1,
    "time": "00:00:00",
    "value": 64
    }
    """
    crt_time = datetime.now()
    if request.form:
        resp = Response("ok")
        resp.headers["Access-Control-Allow-Origin"] = '*'
        data = request.form
        if int(data.get('external')) == 1:
            insert_hr_data([{"time": data["time"], "value": int(data["value"])}], crt_time)
            return resp
        else:
            return resp

    if request.data:
        data = json.loads(request.data)
        heart_rate_series_past_hour = data
    else:
        client_data = HeartRateSensor.query.first()
        client_id, client_secret = client_data.client_id, client_data.client_secret
        token = session.get('oauth_token', None)
        if not token:
            return redirect(url_for('.auth'))
        oauth_session = OAuth2Session(client_id, token=token, scope=['heartrate'])
        heart_rate_response = oauth_session.get(FITBIT_URL.format(str(crt_time.hour), str(crt_time.hour)))
        heart_rate_series_past_hour = heart_rate_response.json()["activities-heart-intraday"]["dataset"]
    created = insert_hr_data(heart_rate_series_past_hour, crt_time)
    return redirect(url_for('user.panel'))



@blueprint.route("/env/fetch", methods=["POST", "GET"])
def get_environment_data():
    """
    Fetching and forwarding environment data from an Android device
{'accelerometer': {'timestamp': 1498765445517, 'Y': -0.024459839, 'Z': 9.765335, 'X': 0.052383423}, 
'magnetometer': {'timestamp': 1498765445310, 'Y': 4.6936035, 'Z': -50.587463, 'X': 19.352722},
 'secret': '9C468FB968', 
 'gyro': {'timestamp': 1498765445413, 'Y': -0.00024414062, 'Z': 0.0016479492, 'X': -0.0018005371}}

    """
    if request.form:
        data = request.form

        parsed_data = data.get("info", None)
        data = json.loads(parsed_data) if parsed_data else data
        resp = Response("ok")
        resp.headers["Access-Control-Allow-Origin"] = '*'

        if int(data.get('external')) == 1:
            insert_env_data(data)
            return resp
        else:
            return resp
    if request.data:
        data = request.data.decode('utf-8').replace('\\', '').replace('"{', '{').replace('}"', '}')
        data = json.loads(data)
        if data["secret"] == MovementSensor.query.first().secret_key:
            insert_env_data(data)
            return "ok", 200
    return "not ok", 404


@blueprint.route("/env/fall", methods=["POST"])
def check_fall():
    resp = Response("ok")
    resp.headers["Access-Control-Allow-Origin"] = '*'
    FallEvent.create()
    return resp


def forward_data(current_cr):
    e = latest_env()
    try:
        ts = float(e.timestamp)
    except ValueError:
        return json.dumps({})
    if datetime.fromtimestamp(ts / 1000) > datetime.now() - timedelta(seconds=10):
        if e:
            grouped = group_env(e)
            corresponding_hr = find_hr_data(ts)
            return json.dumps({
                "user_data": [current_cr.weight, current_cr.height, current_cr.age, current_cr.sex],
                "hr": corresponding_hr.value if corresponding_hr else 0,
                "env": grouped if len(grouped) == 3 else []
            })
    else:
        return json.dumps({})

@blueprint.route("/env/check_fall", methods=["GET", "POST"])
def get_fall_and_level():
    """
    This method gets called from the panel and identifies fall events and activity level checks
    :return: 
    """
    crt = {"code": 1}
    ev = FallEvent.query.first()
    carerecv = CareReceiver.query.first()
    r = forward_data(carerecv)

    try:
        r = requests.get("http://localhost:9000/predict", json=r)
    except requests.exceptions.ConnectionError:
        return jsonify({"code": -1})

    if r.json():
        data = r.json()
        if data["predict"] == "yes" :
            ActivityLevel.create(value=data["result"])
            result = activity_level_mapper[data["result"]]
            crt = {"level": result}
        elif data["predict"] == "no":
            crt = {"code": -1}

    if ev:
        ev.delete()
        crt["fall"] = "yes"
    else:
        crt["fall"] = "no"

    return jsonify(crt)


@blueprint.route("/env/check_hr", methods=["GET", "POST"])
def get_hr():
    hr = latest_hr(date_restricted=True)

    if hr:
        current_cr = CareReceiver.query.first()
        try:
            r = requests.get(
                "http://localhost:9000/heart_status",
                json=json.dumps({"hr": hr.value, "age": current_cr.age, "gender": current_cr.sex})
            )
        except requests.exceptions.ConnectionError:
            return jsonify({"val": -1})
        status = r.json()["status"]
        HeartLevel.create(value=status, hr=hr.value)
        status = hr_mapper[status]
        return jsonify({"val": hr.value, "status":status})
    return jsonify({"val": 0})



