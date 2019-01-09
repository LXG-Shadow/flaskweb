from app import db

class projects_db(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    language = db.Column(db.String(16),nullable=False)
    category = db.Column(db.String(16),nullable=False)
    name = db.Column(db.String(16),nullable=False)
    alias = db.Column(db.String(16), nullable=False)
    desc = db.Column(db.Text,nullable=False)
    type = db.Column(db.Integer,nullable=False)

    @classmethod
    def get(cls,language,category):
        rawdata = cls.query.filter_by(language=language,category=category).all()
        data = []
        for item in rawdata:
            link = "/projects/redirect/%s/%s/%s" % (item.type,item.language,item.alias)
            data.append({"id":item.id,"name":item.name,
                         "desc":item.desc,"type":item.type,
                         "link":link})
        return data

    @classmethod
    def new(cls,language,category,name,alias,desc,type):
        new_project = cls(desc=desc, alias=alias,
                         category=category, language=language,
                         type=type, name=name)
        db.session.add(new_project)
        db.session.commit()