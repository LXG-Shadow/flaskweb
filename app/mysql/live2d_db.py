from app import db
from datetime import datetime, timedelta, timezone

def bjutc():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt

class live2dModel_db(db.Model):
    __tablename__ = "live2dModels"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    path = db.Column(db.String(128), nullable=False)
    upload_time = db.Column(db.DateTime, index=True, default=bjutc)

    @classmethod
    def get_by_id(cls, id):
        rawdata = cls.query.filter_by(id=id).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def get_by_name(cls, name):
        rawdata = cls.query.filter_by(name=name).first()
        if rawdata is None:
            return None
        return rawdata

class live2dTip_db(db.Model):
    __tablename__ = "live2dTips"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    path = db.Column(db.String(128), nullable=False)
    upload_time = db.Column(db.DateTime, index=True, default=bjutc)

    @classmethod
    def get_by_id(cls, id):
        rawdata = cls.query.filter_by(id=id).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def get_by_name(cls, name):
        rawdata = cls.query.filter_by(name=name).first()
        if rawdata is None:
            return None
        return rawdata

class live2dConfig_db(db.Model):
    __tablename__ = "live2dConfigs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    path = db.Column(db.String(128), nullable=False)
    upload_time = db.Column(db.DateTime, index=True, default=bjutc)

    @classmethod
    def get_by_id(cls, id):
        rawdata = cls.query.filter_by(id=id).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def get_by_name(cls, name):
        rawdata = cls.query.filter_by(name=name).first()
        if rawdata is None:
            return None
        return rawdata