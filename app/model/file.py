from .mysql.file_db import file_db
from flask import current_app


class file(object):
    def __init__(self, id, alias, description, permission, external, link, password, upload_time):
        self.id = id
        self.alias = alias
        self.description = description
        self.permission = permission
        self.external = external
        self.link = link
        self.password = password
        self.upload_time = upload_time

    @classmethod
    def initFromId(cls, id):
        data = file_db.get_by_id(id)
        if data is None:
            return cls(None, None, None, None, None, None, None, None)
        return cls(data.id, data.alias, data.description, data.permission, data.external, data.link, data.password,
                   data.upload_time)

    @classmethod
    def initFromAlias(cls, alias):
        data = file_db.get_by_alias(alias)
        if data is None:
            return cls(None, None, None, None, None, None, None, None)
        return cls(data.id, data.alias, data.description, data.permission, data.external, data.link, data.password,
                   data.upload_time)

    @classmethod
    def upload(cls, alias, description, permission, external, link, password):
        if not file_db.get_by_alias(alias) is None:
            return (False, 21)
        try:
            data = file_db.insert(alias, description, permission, external, link, password)
            return (True, 19, data.id)
        except:
            return (False, -3)

    @classmethod
    def edit(cls, id, alias, description, permission, external, link, password):
        data = file_db.get_by_alias(alias)
        if not data is None:
            if data.id != id:
                return (False, 21)
        try:
            data = file_db.edit(id, alias, description, permission, external, link, password)
            # 基本不会出现的情景
            if data is None:
                return (False, 17)
            return (True, 20, data.id)
        except:
            return (False, -3)

    @classmethod
    def delete(cls, id):
        try:
            data = file_db.remove(id)
            if not data:
                return (False, 17)
            return (True, 18)
        except:
            return (False, -3)

    def isAccessible(self, user):
        if user.group.permission >= self.permission:
            return True
        else:
            return False

    def isNone(self):
        return not bool(self.id)


class files(object):
    def __init__(self, pagination):
        self.pagination = pagination

    @classmethod
    def initFromAll(cls, page, desc=True):
        if desc:
            pagination = file_db.query.order_by(file_db.upload_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = file_db.query.order_by(file_db.upload_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination)

    @classmethod
    def initFromPara(cls, page, desc=True, **parameters):
        if desc:
            pagination = file_db.query.filter_by(**parameters).order_by(file_db.upload_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = file_db.query.filter_by(**parameters).order_by(file_db.upload_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)

        return cls(pagination)

    def isNone(self):
        if len(self.pagination.items) == 0:
            return True
        else:
            return False
