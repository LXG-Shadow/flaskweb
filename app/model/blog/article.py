from app.model.mysql.blog import article_db
from flask import current_app


class article(object):

    def __init__(self, id, title, content_raw, content, summary, create_time, updated_time, num_of_view, type, source,
                 user):
        self.id = id
        self.title = title
        self.content_raw = content_raw
        self.content = content
        self.summary = summary
        self.create_time = create_time
        self.update_time = updated_time
        self.num_of_view = num_of_view
        self.type = type
        self.source = source
        self.user = user

    @classmethod
    def initFromId(cls, id):
        data = article_db.get_by_id(id)
        if data is None:
            return cls(None, None, None, None, None, None, None, None, None, None, None)
        return cls(data.id, data.title, data.content_raw, data.content, data.summary, data.create_time,
                   data.update_time, data.num_of_view,
                   data.type, data.source, data.user)

    @classmethod
    def initFromTitle(cls, title):
        data = article_db.get_by_title(title)
        if data is None:
            return cls(None, None, None, None, None, None, None, None, None, None, None)
        return cls(data.id, data.title, data.content_raw, data.content, data.summary, data.create_time,
                   data.update_time, data.num_of_view,
                   data.type, data.source, data.user)

    @classmethod
    def initNone(cls):
        return cls(None, None, None, None, None, None, None, None, None, None, None)

    @staticmethod
    def add(title, content_raw, summary, type_id, source_id, user_id,advanced = False):
        if not article_db.get_by_title(title) is None:
            return (False, 11)
        try:
            data = article_db.insert_article(title, content_raw, summary, type_id, source_id, user_id,advanced)
            return (True, 12, data.id)
        except:
            return (False, -3)

    @staticmethod
    def edit(id, title, content_raw, summary, type_id, source_id,advanced = False):
        data = article_db.get_by_title(title)
        if not data is None:
            if data.id != id:
                return (False, 11)
        try:
            data = article_db.edit_article(id, title, content_raw, summary, type_id, source_id,advanced)
            # 基本不会出现的情景
            if data is None:
                return (False, 13)
            return (True, 14, data.id)
        except:
            return (False, -3)

    @staticmethod
    def delete(id):
        try:
            data = article_db.delete_article(id)
            if data is None:
                return (False, 13)
            return (True, 15)
        except:
            return (False, -3)

    @staticmethod
    def get_total_num():
        return article_db.query.count()

    def is_none(self):
        if self.id is None:
            return True
        else:
            return False

    def is_protected(self):
        if self.type:
            return self.type.setting.protected
        else:
            return False

    def is_hide(self):
        if self.type:
            return self.type.setting.hide
        else:
            return False

    def add_view(self):
        data = article_db.add_view(self.id)
        if not data is None:
            self.num_of_view = data.num_of_view
        else:
            pass


class articles(object):
    def __init__(self,pagination):
        self.pagination = pagination

    @classmethod
    def initFromAll(cls, page, desc=True):
        if desc:
            pagination = article_db.query.order_by(article_db.create_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = article_db.query.order_by(article_db.create_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination)

    @classmethod
    def initFromUser(cls, id, page, desc=True):
        if desc:
            pagination = article_db.query.filter_by(user_id=id).order_by(article_db.create_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = article_db.query.filter_by(user_id=id).order_by(article_db.create_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination)

    @classmethod
    def initFromPara(cls, page, desc=True,**parameters):
        if desc:
            pagination = article_db.query.filter_by(**parameters).order_by(article_db.create_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = article_db.query.filter_by(**parameters).order_by(article_db.create_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination)

    def isNone(self):
        if len(self.pagination.items) == 0:
            return True
        else:
            return False
