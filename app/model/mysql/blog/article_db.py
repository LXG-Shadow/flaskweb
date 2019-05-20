from app import db
from datetime import datetime, timedelta, timezone
import bleach
from markdown import markdown


def bjutc():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt


class articleSource_db(db.Model):
    __tablename__ = 'articleSources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('article_db', backref='source', lazy='dynamic')

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
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def init_sources(cls):
        sources = (u'原创',
                   u'转载',
                   u'翻译')
        for s in sources:
            source = cls.query.filter_by(name=s).first()
            if source is None:
                source = cls(name=s)
            db.session.add(source)
        db.session.commit()

    @classmethod
    def insert(cls, s):
        source = cls.query.filter_by(name=s).first()
        if source is None:
            source = cls(name=s)
            db.session.add(source)
            db.session.commit()
            return True
        else:
            return False


class articleTypeSetting(db.Model):
    __tablename__ = 'articleTypeSettings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    protected = db.Column(db.Boolean, default=False)
    hide = db.Column(db.Boolean, default=False)
    types = db.relationship('articleType_db', backref='setting', lazy='dynamic')

    @classmethod
    def init_default_settings(cls):
        system_setting = cls(name='system', protected=True, hide=True)
        common_setting = cls(name='common', protected=False, hide=False)
        db.session.add(system_setting)
        db.session.add(common_setting)
        db.session.commit()

    @classmethod
    def insert_settings(cls, name, protected, hide):
        setting = cls(name=name, protected=protected, hide=hide)
        db.session.add(setting)
        db.session.commit()


class articleType_db(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.Text, default=None)
    articles = db.relationship('article_db', backref='type', lazy='dynamic')
    # menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), default=None)
    setting_id = db.Column(db.Integer, db.ForeignKey('articleTypeSettings.id'))

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
    def init_system_articleType(cls):
        articleType = cls(name=u'默认分类',
                          introduction=u'系统默认分类',
                          setting=articleTypeSetting.query.filter_by(name='system').first()
                          )
        db.session.add(articleType)
        db.session.commit()

    @classmethod
    def getAll(cls):
        return cls.query.all()

    @classmethod
    def insert(cls, t):
        type = cls.query.filter_by(name=t).first()
        if type is None:
            type = cls(name=t)
            db.session.add(type)
            db.session.commit()
            return True
        return False


class articleTags_db(db.Model):
    __tablename__ = "articleTags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True,index=True)

    @classmethod
    def select_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def select_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def insert(cls, name):
        tag = cls.select_by_name(name)
        if tag == None:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
        return tag


class articletagLink_db(db.Model):
    __tablename__ = "articletagLink"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), index=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('articleTags.id'), index=True)

    @classmethod
    def select_by_articleId(cls, aid):
        return cls.query.filter_by(article_id=aid).all()

    @classmethod
    def select_by_tagId(cls,tid):
        return cls.query.filter_by(tag_id = tid).all()

    @classmethod
    def insert(cls, aid, tid):
        l = cls(article_id=aid, tag_id=tid)
        db.session.add(l)
        db.session.commit()
        return l

    @classmethod
    def delete(cls, aid, tid):
        l = cls.query.filter_by(article_id=aid, tag_id=tid).first()
        if l == None:
            return
        db.session.delete(l)
        db.session.commit()
        return


class article_db(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    content_raw = db.Column(db.Text)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=bjutc)
    update_time = db.Column(db.DateTime, index=True, default=bjutc)
    num_of_view = db.Column(db.Integer, default=0)
    type_id = db.Column(db.Integer, db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('articleSources.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('userstable.id'))

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def insert(cls, title, content_raw, summary, type_id, source_id, user_id, advanced):
        article = cls(title=title, content_raw=content_raw, summary=summary,
                      type_id=type_id, source_id=source_id, user_id=user_id)
        db.session.add(article)
        if advanced:
            article.content = cls.markdown(article.content_raw)
        db.session.commit()
        return article

    @classmethod
    def delete(cls, id):
        article = cls.get_by_id(id)
        if article is None:
            return None
        db.session.delete(article)
        db.session.commit()
        return True

    @classmethod
    def edit(cls, id, title, content_raw, summary, type_id, source_id, advanced):
        article = cls.get_by_id(id=id)
        if article is None:
            return None
        article.title = title
        article.content_raw = content_raw
        article.summary = summary
        article.update_time = bjutc()
        article.type_id = type_id
        article.source_id = source_id
        if advanced:
            article.content = cls.markdown(article.content_raw)
        db.session.commit()
        return article

    @classmethod
    def add_view(cls, id):
        article = cls.get_by_id(id=id)
        if article is None:
            return None
        article.num_of_view += 1
        db.session.commit()
        return article

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        # 需要转换的标签
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
            'h1', 'h2', 'h3', "h4", "h5", 'p', 'img', 'br', "del", "hr"
        ]
        # 需要提取的标签属性，否则会被忽略掉
        attrs = {
            '*': ['class'],
            'a': ['href', 'rel'],
            'img': ['src', 'alt']
        }
        target.content = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allowed_tags,
                attributes=attrs,
                strip=True
            )
        )

    @staticmethod
    def markdown(content_raw):
        return markdown(content_raw, output_format='html')
