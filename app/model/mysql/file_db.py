from app import db
from datetime import datetime, timedelta, timezone

def bjutc():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt

class file_db(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alias = db.Column(db.String(16), nullable=False)
    description = db.Column(db.Text)
    permission = db.Column(db.Integer, default=0)
    external = db.Column(db.Boolean, default=False)
    link = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(16),nullable=True)
    upload_time = db.Column(db.DateTime, index=True, default=bjutc)

    @classmethod
    def get_by_id(cls, id):
        rawdata = cls.query.filter_by(id=id).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def get_by_alias(cls, alias):
        rawdata = cls.query.filter_by(alias=alias).first()
        if rawdata is None:
            return None
        return rawdata

    @classmethod
    def insert(cls,alias,description,permission,external,link,password):
        file = cls(alias=alias,description=description,permission=permission,
                   external=external,link=link,password=password)
        db.session.add(file)
        db.session.commit()
        return file

    @classmethod
    def remove(cls, id):
        file = cls.get_by_id(id)
        if file is None:
            return False
        db.session.delete(file)
        db.session.commit()
        return True

    @classmethod
    def edit(cls, id,alias,description,permission,external,link,password):
        file = cls.get_by_id(id)
        if file is None:
            return None
        file.alias = alias
        file.description = description
        file.permission = permission
        file.external = external
        file.link = link
        file.password = password

        db.session.commit()
        return file