# -*- coding: utf-8 -*-
import json
from base64 import standard_b64encode

import dataset
from datetime import datetime

import requests
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app, session, jsonify)
from flask_login import login_required
from requests_oauthlib import OAuth2Session

from ..constants import authorization_base_url, FITBIT_URL
from ..models.env_data import FallEvent, ActivityLevel, HeartLevel, MovementSensor, HeartRateSensor
from ..utils import insert_env_data, insert_hr_data, latest_hr, find_env_data

blueprint = Blueprint("api", __name__, url_prefix='/api',
                      static_folder="../static")

@blueprint.route("/hr/auth", methods=["POST"])
@login_required
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
@login_required
def hr():
    """Step 3: Fetching a protected resource using an OAuth 2 token. (in this case the intraday heartrate)
    """
    crt_time = datetime.now()
    if request.data:
        heart_rate_series_past_hour = json.loads(request.data)
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
    if created:
        return "Accepted, {} rows inserted".format(created), 200
    return "All done", 200


@blueprint.route("/env/fetch", methods=["POST", "GET"])
def get_environment_data():
    """
    Fetching and forwarding environment data from an Android device
    :return: 
    """
    if request.data:
        data = request.data.decode('utf-8').replace('\\', '').replace('"{', '{').replace('}"', '}')
        data = json.loads(data)
        if data["secret"] == MovementSensor.query.first().secret_key:
            insert_env_data(data)
            return "Accepted", 200
    return "Wrong endpoint", 404

@blueprint.route("/env/fall", methods=["POST", "GET"])
@login_required
def check_fall():
    if request.data:
        FallEvent.create()
        return "Fall registered", 200
    return "Wrong call", 404


@blueprint.route("/env/check_fall", methods=["POST"])
@login_required
def get_fall():
    ev = FallEvent.query.first()

    if ev:
        ev.delete()
        return jsonify({"fall": "yes"})
    return jsonify({"fall": "no"})


