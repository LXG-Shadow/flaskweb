from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone


def bjutc():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt


class userGroup_db(db.Model):
    __tablename__ = "userGroups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    permission = db.Column(db.Integer, nullable=False)
    users = db.relationship('user_db', backref='group', lazy='dynamic')

    @classmethod
    def getAlluserGroup(cls):
        return cls.query.all()

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

    @classmethod
    def init_userGroups(cls):
        admin = cls(name=u'Admin', permission=3)
        advanceduser = cls(name=u'Advanced User', permission=2)
        user = cls(name=u'User', permission=1)
        guest = cls(name=u'Guest', permission=0)
        db.session.add(admin)
        db.session.add(advanceduser)
        db.session.add(user)
        db.session.add(guest)
        db.session.commit()

    @classmethod
    def insert_userGroup(cls, g, p):
        group = cls.query.filter_by(name=g).first()
        if group is None:
            group = cls(name=g, permission=p)
            db.session.add(group)
            db.session.commit()
            return True
        return False


class user_db(db.Model):
    __tablename__ = "userstable"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(31), nullable=False)
    register_time = db.Column(db.DateTime, index=True, default=bjutc)
    articles = db.relationship('article_db', backref='user', lazy='dynamic')
    group_id = db.Column(db.Integer, db.ForeignKey('userGroups.id'))

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

    @classmethod
    def get_by_email(cls, email):
        rawdata = cls.query.filter_by(email=email).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def new(cls, name, password, email, group_id=3):
        new_user = cls(name=name, password=generate_password_hash(password),
                       email=email, group_id=group_id)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def edit_user(cls, id, name, email, password=None, group_id=None):
        user = cls.get_by_id(id=id)
        if user is None:
            return None
        user.name = name
        user.email = email
        if group_id:
            user.group_id = group_id
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()
        return user
