# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import requests
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app)

from flask_login import login_required, logout_user, current_user

from ..constants import activity_level_mapper, hr_mapper
from ..models.env_data import MovementSensor, HeartRateSensor, HeartData, ActivityLevel, HeartLevel
from pulser.utils import flash_errors, render_extensions, latest_hr, find_env_data, latest_env, find_hr_data, group_env
from pulser.forms.user import PasswordForm, EmailForm, UsernameForm, MovementSensorForm, HrSensorForm, CareReceiverForm
from pulser.extensions import mail
from pulser.models.user import User, CareReceiver
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/")
@login_required
def profile():
    return render_extensions("users/profile.html", user=current_user)

@blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        emailuser = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"
        from pulser.settings import Config

        ts = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = ts.dumps(emailuser.email, salt='recover-key')

        recover_url = url_for('user.reset_with_token', token=token, _external=True)
        html = render_template('email/recover.html', recover_url=recover_url)

        msg = Message(html=html, recipients=[emailuser.email], subject=subject)
        mail.send(msg)

        return redirect(url_for('public.home'))
    else:
        flash_errors(form)

    return render_extensions('users/reset.html', resetform=form)

@blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        from pulser.settings import Config

        ts = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        return render_template("404.html")

    form = PasswordForm()

    if form.validate_on_submit():
        emailuser = User.query.filter_by(email=email).first_or_404()
        emailuser.set_password(form.password.data)
        emailuser.save()
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)

    return render_extensions('users/reset_with_token.html', resetform=form, token=token)


@blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        current_user.save()
        return redirect(url_for('user.profile'))
    else:
        flash_errors(form)

    return render_extensions('users/change_password.html', resetform=form)


@blueprint.route('/connections', methods=['GET', 'POST'])
@login_required
def connections():
    move = MovementSensor.query.first()
    hr = HeartRateSensor.query.first()
    cr = CareReceiver.query.first()
    print(move, hr)
    return render_extensions('users/connections.html', movement_sensor=move, hr_sensor=hr, carereceiver=cr)

def forward_data():
    e = latest_env()
    ts = float(e.timestamp)
    if datetime.fromtimestamp(ts / 1000) > datetime.now() - timedelta(minutes=1):
        if e:
            grouped = group_env(e)
            corresponding_hr = find_hr_data(ts)
            current_cr =  CareReceiver.query.first()
            return json.dumps({
                "user_data": [current_cr.weight, current_cr.height, current_cr.age, current_cr.sex],
                "hr": corresponding_hr.value if corresponding_hr else 0,
                "env": grouped if len(grouped) == 3 else []
            })
    else:
        return json.dumps({"err_env": True})


@blueprint.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():

    r = forward_data()

    carerecv = CareReceiver.query.first()
    print(json.loads(r))
    if json.loads(r).get("err_env", None):
        flash("Environment data is not registered correctly. Check the movement sensor.", "warning")
        return render_extensions('users/panel.html',
                                 carereceiver=carerecv,
                                 level=None, hr=None)
    elif json.loads(r).get("hr", 0) == 0:
        flash("Heart data is too old for accurate prediction. "
              "Check the heart rate sensor is correctly placed and synced. (press refresh to re-sync manually)", "warning")

    try:
        r = requests.get("http://localhost:9000/predict", json=r)
    except requests.exceptions.ConnectionError:
        flash("Unable to retrieve activity level and heart data", "danger")
        return render_extensions('users/panel.html',
                                 carereceiver=carerecv,
                                 level=None, hr=None)

    if r.json():
        data = r.json()
        if data["predict"] == "yes" and data["result"] != -1:
            ActivityLevel.create(value=data["result"])
            HeartLevel.create(value=data["hr_stat"], hr=data["hr"])
        elif data["predict"] == "no" and data["result"] != -1:
            HeartLevel.create(value=data["hr_stat"], hr=data["hr"])


    hr = HeartLevel.query.order_by(HeartLevel.created_at.desc()).first()
    level = ActivityLevel.query.order_by(ActivityLevel.created_at.desc()).first()
    return render_extensions('users/panel.html',
                             carereceiver=carerecv,
                             level=activity_level_mapper[level.value] if level else None,
                             hr=hr_mapper[hr.value] if hr else None)


@blueprint.route('/connect_move', methods=['GET', 'POST'])
@login_required
def connect_move():
    form = MovementSensorForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        MovementSensor.create(secret_key=form.secret_key.data)
        flash("Successfully connected movement sensor!", 'success')
        return redirect(url_for('user.connections'))
    else:
        flash_errors(form)
    return render_extensions('users/connect_movement_sensor.html', form=form)

@blueprint.route('/disconnect_move', methods=['GET', 'POST'])
@login_required
def disconnect_move():
    MovementSensor.query.first().delete()
    flash("Successfully disconnected movement sensor!", 'success')
    return redirect(url_for('user.connections'))


@blueprint.route('/connect_hr', methods=['GET', 'POST'])
@login_required
def connect_hr():
    form = HrSensorForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        HeartRateSensor.create(client_id=form.client_id.data, client_secret=form.client_secret.data)
        flash("Successfully connected movement sensor!", 'success')
        return redirect(url_for('user.connections'))
    else:
        flash_errors(form)
    return render_extensions('users/connect_hr_sensor.html', form=form)

@blueprint.route('/disconnect_hr', methods=['GET', 'POST'])
@login_required
def disconnect_hr():
    HeartRateSensor.query.first().delete()
    flash("Successfully disconnected heart rate sensor!", 'success')
    return redirect(url_for('user.connections'))


@blueprint.route('/connect_cr', methods=['GET', 'POST'])
@login_required
def connect_cr():
    form = CareReceiverForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = CareReceiver.create(
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               age=int(form.age.data),
                               weight=int(form.weight.data),
                               height=int(form.height.data),
                               sex=int(form.sex.data))
        flash("Successfully added a caregiver!", 'success')
        return redirect(url_for('user.connections'))
    else:
        flash_errors(form)
    return render_extensions('users/connect_carerecv.html', form=form)

@blueprint.route('/disconnect_cr', methods=['GET', 'POST'])
@login_required
def disconnect_cr():
    CareReceiver.query.first().delete()
    HeartRateSensor.query.first().delete()
    MovementSensor.query.first().delete()

    flash("Successfully unregistered care receiver!", 'success')
    return redirect(url_for('user.connections'))

