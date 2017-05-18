import datetime as dt

from pulser.extensions import db
from pulser.models.relationships import tags_posts
from pulser.database import (
    Column,
    Model,
    SurrogatePK,
)

class FallEvent(SurrogatePK, Model):
    __tablename__ = 'fall_event'

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)


class MovementSensor(SurrogatePK, Model):
    __tablename__ = 'movement_sensor'

    secret_key = db.Column(db.Text)


class HeartRateSensor(SurrogatePK, Model):
    __tablename__ = 'hr_sensor'

    client_id = db.Column(db.Text)
    client_secret = db.Column(db.Text)


class EnvData(SurrogatePK, Model):

    __tablename__ = 'env'

    sensor_type = db.Column(db.Text)
    x = db.Column(db.Text)
    y = db.Column(db.Text)
    z = db.Column(db.Text)
    timestamp = db.Column(db.BigInteger)
    group = db.Column(db.Integer)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class HeartData(SurrogatePK, Model):

    __tablename__ = 'hr'

    timestamp = db.Column(db.Text)
    value = db.Column(db.Integer)
    sent = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)


class ActivityLevel(SurrogatePK, Model):

    __tablename__ = 'activ_lvl'

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    value = db.Column(db.Integer) # Ranges from 1 to 3: Low, Medium and High

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

class HeartLevel(SurrogatePK, Model):

    __tablename__ = 'heart_lvl'

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    value = db.Column(db.Integer) # Ranges from 1 to 0: Good and not Ideal
    hr = db.Column(db.Integer)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)