from flask import current_app
from app.model.mysql import user_db, userGroup_db
from werkzeug.security import check_password_hash
from base64 import urlsafe_b64encode


class userGroup(object):
    def __init__(self, id, name, permission):
        self.id = id
        self.name = name
        self.permission = permission

    @classmethod
    def initFromId(cls, id=4):
        data = userGroup_db.get_by_id(id)
        if data is None:
            data = userGroup_db.get_by_id(id)
        return cls(data.id, data.name, data.permission)

    @classmethod
    def initFromName(cls, name="Guest"):
        data = userGroup_db.get_by_name(name)
        if data is None:
            data = userGroup_db.get_by_id(name)
        return cls(data.id, data.name, data.permission)

    @classmethod
    def initFromModel(cls, model):
        return cls(model.id, model.name, model.permission)

    @classmethod
    def initGuest(cls):
        return cls(4, "Guest", 0)


class user(object):

    def __init__(self, id, name, password, email, group):
        self.id = id
        self.name = name
        self.__password = password
        self.email = email
        self.group = group

    # initFromCookie

    @classmethod
    def initFromId(cls, id):
        data = user_db.get_by_id(id)
        if data is None:
            return cls(None, None, None, None, userGroup.initGuest())
        return cls(data.id, data.name, data.password, data.email, userGroup.initFromModel(data.group))

    @classmethod
    def initFromName(cls, name):
        data = user_db.get_by_name(name)
        if data is None:
            return cls(None, None, None, None, userGroup.initGuest())
        return cls(data.id, data.name, data.password, data.email, userGroup.initFromModel(data.group))

    @classmethod
    def initFromEmail(cls, email):
        data = user_db.get_by_email(email)
        if data is None:
            return cls(None, None, None, None, userGroup.initGuest())
        return cls(data.id, data.name, data.password, data.email, userGroup.initFromModel(data.group))

    @classmethod
    def initNone(cls):
        return cls(None, None, None, None, userGroup.initGuest())

    @staticmethod
    def register(name, password, email, group_id=None):
        if not user_db.get_by_name(name) is None:
            return (False, 4)
        if not user_db.get_by_email(email) is None:
            return (False, 5)
        try:
            if group_id:
                data = user_db.new(name, password, email, group_id=group_id)
            else:
                data = user_db.new(name, password, email)
            return (True, 6, data.id)
        except:
            return (False, -3)

    @staticmethod
    def edit(id, name, email, group_id=None, password=None):
        user = user_db.get_by_name(name)
        if not user is None:
            if user.id != id:
                return (False, 4)
        user = user_db.get_by_email(email)
        if not user is None:
            if user.id != id:
                return (False, 5)
        try:
            user_db.edit_user(id, name, email, group_id=group_id, password=password)
            return (True, 16)
        except:
            return (False, -3)

    def getGroup(self):
        return userGroup_db.get_by_id(self.group.id)

    def is_anonymous(self):
        if self.id is None:
            return True
        else:
            return False

    def is_authenticate(self, psd):
        return check_password_hash(self.__password, psd)

    def getAuthString(self, password):
        return urlsafe_b64encode("_".join([str(self.id), password]).encode('utf-8'))


class users(object):
    def __init__(self, pagination):
        self.pagination = pagination

    @classmethod
    def initFromAll(cls, page, desc=False):
        if desc:
            pagination = user_db.query.order_by(user_db.register_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = user_db.query.order_by(user_db.register_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination)

    @classmethod
    def initFromGroup(cls, group_id, page, desc=True):
        if desc:
            pagination = article_db.query.filter_by(user_id=id).order_by(article_db.create_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
            articles = pagination.items
        else:
            pagination = article_db.query.filter_by(user_id=id).order_by(article_db.create_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
            articles = pagination.items
        return cls(articles, pagination)

    def isNone(self):
        if len(self.pagination.items) == 0:
            return True
        else:
            return False
