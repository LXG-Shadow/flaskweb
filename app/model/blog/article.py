from app.mysql import article_db, articleSource_db, articletagLink_db, articleTags_db
from app.mysql.user_db import user_db
from flask import current_app


class article(object):

    def __init__(self, id, title, content_raw, content, summary, create_time, updated_time, num_of_view, type, source,
                 user, tags):
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
        self.tags = tags

    @classmethod
    def initFromId(cls, id):
        data = article_db.get_by_id(id)
        if data is None:
            return cls.initNone()
        tags = [articleTags_db.select_by_id(r.tag_id) for r in articletagLink_db.select_by_articleId(data.id)]
        return cls(data.id, data.title, data.content_raw, data.content, data.summary, data.create_time,
                   data.update_time, data.num_of_view,
                   data.type, articleSource_db.get_by_id(data.source_id), user_db.get_by_id(data.user_id), tags)

    @classmethod
    def initFromTitle(cls, title):
        data = article_db.get_by_title(title)
        if data is None:
            return cls.initNone()
        # 获取tag
        tags = [articleTags_db.select_by_id(r.tag_id) for r in articletagLink_db.select_by_articleId(data.id)]
        return cls(data.id, data.title, data.content_raw, data.content, data.summary, data.create_time,
                   data.update_time, data.num_of_view,
                   data.type, articleSource_db.get_by_id(data.source_id), user_db.get_by_id(data.user_id), tags)

    @classmethod
    def initFromObject(cls, obj):
        tags = [articleTags_db.select_by_id(r.tag_id) for r in articletagLink_db.select_by_articleId(obj.id)]
        return cls(obj.id, obj.title, obj.content_raw, obj.content, obj.summary, obj.create_time,
                   obj.update_time, obj.num_of_view,
                   obj.type, articleSource_db.get_by_id(obj.source_id), user_db.get_by_id(obj.user_id), tags)

    @classmethod
    def initNone(cls):
        return cls(None, None, None, None, None, None, None, None, None, None, None, [])

    @staticmethod
    def add(title, content_raw, summary, type_id, source_id, user_id, tags, advanced=False):
        if not article_db.get_by_title(title) is None:
            return (False, 11)
        try:
            data = article_db.insert(title, content_raw, summary, type_id, source_id, user_id, advanced)
            # 添加 tag
            for tag in tags:
                t = articleTags_db.insert(tag)
                articletagLink_db.insert(data.id, t.id)
            return (True, 12, data.id)
        except:
            return (False, -3)

    @staticmethod
    def edit(id, title, content_raw, summary, type_id, source_id, tags, advanced=False):
        data = article_db.get_by_title(title)
        if not data is None:
            if data.id != id:
                return (False, 11)
        try:
            data = article_db.edit(id, title, content_raw, summary, type_id, source_id, advanced)
            # 基本不会出现的情景
            if data is None:
                return (False, 13)
            tags0 = [articleTags_db.select_by_id(r.tag_id).name for r in articletagLink_db.select_by_articleId(data.id)]
            # 添加新的
            for tag in set(tags) - set(tags0):
                t = articleTags_db.insert(tag)
                articletagLink_db.insert(data.id, t.id)
            # 删除没有的
            for tag in set(tags0) - set(tags):
                articletagLink_db.delete(data.id, articleTags_db.select_by_name(tag).id)
            return (True, 14, data.id)
        except:
            return (False, -3)

    @staticmethod
    def delete(id):
        try:
            data = article_db.delete(id)
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
    def __init__(self, page, per_page, total, items):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = int((total-1) / per_page) + 1
        self.items = [article.initFromObject(obj) for obj in items]


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
        return cls(pagination.page, pagination.per_page, pagination.total, pagination.items)

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
        return cls(pagination.page, pagination.per_page, pagination.total, pagination.items)

    @classmethod
    def initFromTag(cls, tag, page, desc=True):
        tag = articleTags_db.select_by_name(tag)
        if tag == None:
            return cls(page, 10, 0, [])
        tags = articletagLink_db.select_by_tagId(tag.id)
        # 按博客发表时间排序
        tags.sort(key=lambda t:t.article_id)
        per_page = current_app.config['ITEMS_PER_PAGE']
        total = len(tags)
        if desc:
            tags.reverse()
        items = [article_db.get_by_id(tag.article_id) for tag in tags[(page-1)*per_page:page*per_page:]]
        return cls(page, per_page, total, items)

    @classmethod
    def initFromPara(cls, page, desc=True, **parameters):
        if desc:
            pagination = article_db.query.filter_by(**parameters).order_by(article_db.create_time.desc()).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        else:
            pagination = article_db.query.filter_by(**parameters).order_by(article_db.create_time).paginate(
                page, per_page=current_app.config['ITEMS_PER_PAGE'],
                error_out=False)
        return cls(pagination.page, pagination.per_page, pagination.total, pagination.items)

    def isNone(self):
        if len(self.items) == 0:
            return True
        else:
            return False
