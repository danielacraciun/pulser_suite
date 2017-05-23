# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash, render_template, current_app
from datetime import datetime
from time import strptime

from .models.env_data import EnvData, HeartData


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                  .format(getattr(form, field).label.text, error), category)


def render_extensions(template_path, **kwargs):
    """
    Wraps around the standard render template method and shoves in some other stuff out of the config.

    :param template_path:
    :param kwargs:
    :return:
    """

    return render_template(template_path,
                           _GOOGLE_ANALYTICS=current_app.config['GOOGLE_ANALYTICS'],
                           **kwargs)

def get_next_group_id():
    result = EnvData.query.order_by(EnvData.group.desc()).first()
    return result.group + 1 if result else 1

def insert_env_data(data):
    group_id = get_next_group_id()
    data.pop("secret")
    for data_type in data.keys():
        EnvData.create(
            sensor_type=data_type, x=data[data_type]["X"],
            y=data[data_type]["Y"], z=data[data_type]["Z"],
            group=group_id, timestamp=data[data_type]["timestamp"])

def find_env_data(given_date=None):
    to_dict = []
    if given_date:
        result = EnvData.query.order_by(EnvData.timestamp.desc()).all()
        for env_data in result:
            if abs(float(env_data.timestamp)/1000 - float(given_date)) < 100:
                grouped = EnvData.query.filter_by(group=env_data.group).all()
                ls = list(grouped)
                for elem in ls:
                    to_dict.append({"type": elem.sensor_type,"x": elem.x, "y": elem.y, "z":elem.z, "timestamp": elem.timestamp})
                break
    else:
        ls = list(EnvData.query.order_by(EnvData.timestamp.desc()).limit(20).all())
        for elem in ls:
            to_dict.append({"type": elem.sensor_type, "x": elem.x, "y": elem.y, "z":elem.z, "timestamp": elem.timestamp, "group":elem.group})
    return to_dict

def insert_hr_data(data, now: datetime):
    new_data = 0
    for hr in data:
        f_time = strptime(hr["time"], "%H:%M:%S")
        t = datetime(
            now.year, now.month, now.day, f_time.tm_hour, f_time.tm_min, f_time.tm_sec).timestamp()
        if not HeartData.query.filter_by(timestamp=t).first():
            HeartData.create(timestamp=t, value=int(hr["value"]), sent=False)
            new_data += 1
    return new_data


def latest_hr():
    """ Send earliest hr data that hasn't been sent yet, we don't care about matching with env data
        because we provide a resource """
    hr_obj = HeartData.query.filter_by(sent=False).order_by(HeartData.timestamp.desc()).first()
    if hr_obj:
        hr_obj.sent = True
        hr_obj.save()
        return hr_obj

def latest_env():
    return EnvData.query.order_by(EnvData.timestamp.desc()).first()

def find_hr_data(given_date=None):
    result = HeartData.query.order_by(HeartData.timestamp.desc()).all()
    for hr in result:
        if abs(float(hr.timestamp) - float(given_date) * 1000) < 100:
            return hr

def group_env(env_data):
    data = []
    grouped = EnvData.query.filter_by(group=env_data.group).all()
    ls = list(grouped)
    for elem in ls:
        data.append(
            {"type": elem.sensor_type, "x": elem.x, "y": elem.y, "z": elem.z, "timestamp": elem.timestamp})
    return data