from flask_wtf import Form,FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields import StringField,TextAreaField,SubmitField,PasswordField,BooleanField,RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from ...model.mysql.user_db import userGroup_db
from ...model.mysql.blog.article_db import articleSource_db,articleType_db

class UserEditForm(FlaskForm):
    id = StringField(u'Id')
    username = StringField(u'Username', validators=[DataRequired(), Length(4, 16)])
    password = StringField(u"Password")
    email = StringField(u'Email', validators=[DataRequired(), Email(),Length(7, 31)])
    group = QuerySelectField(u"用户组", query_factory=userGroup_db.getAlluserGroup, get_label="name")
    submit = SubmitField(u'更新资料')


class UserRegisterForm(FlaskForm):
    id = StringField(u'Id')
    username = StringField(u'Username', validators=[DataRequired(), Length(4, 16)])
    password = StringField(u"Password",validators=[DataRequired(), Length(5, 16)])
    email = StringField(u'Email', validators=[DataRequired(), Email(),Length(7, 31)])
    group = QuerySelectField(u"用户组", query_factory=userGroup_db.getAlluserGroup, get_label="name")
    submit = SubmitField(u'新增用户')


class PageDownForm(FlaskForm):
    title = StringField(u"标题", validators=[DataRequired(),Length(1, 64)])
    source = QuerySelectField(u"来源",query_factory=articleSource_db.getAllarticleSource,get_label="name")
    type = QuerySelectField(u"类型",query_factory=articleType_db.getAllarticleType,get_label="name")
    summary = TextAreaField(u"简介", validators=[DataRequired()])
    content = PageDownField(u"Enter MarkDown Text",validators=[DataRequired()])
    no_clean = None
    submit = SubmitField(u'Submit')

class AdvancedPageDownForm(PageDownForm):
    no_clean = BooleanField(u"使用高级模式")

class FileEditForm(FlaskForm):
    id = StringField(u'Id')
    alias = StringField(u'Alias', validators=[DataRequired(), Length(1, 16)])
    description = TextAreaField("简介")
    external = BooleanField(u"是否外链",default=True)
    permission = QuerySelectField(u"获取权限", query_factory=userGroup_db.getAlluserGroup, get_label="name")
    link = StringField(u"Link")
    password = StringField(u"Password")
    submit = SubmitField(u'修改信息')

class FileUploadForm(FileEditForm):
    submit = SubmitField(u'添加新的文件')

class DeleteForm(FlaskForm):
    id = StringField(u"id")
    submit = SubmitField(u"确认删除")
