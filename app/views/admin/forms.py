from flask_wtf import Form,FlaskForm
from flask_babel import lazy_gettext as _l
from flask_pagedown.fields import PageDownField
from wtforms.fields import StringField,TextAreaField,SubmitField,PasswordField,BooleanField,RadioField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from ...model.mysql.user_db import userGroup_db
from ...model.mysql.blog.article_db import articleSource_db,articleType_db

class UserEditForm(FlaskForm):
    id = StringField(u'Id')
    username = StringField(_l('Username'), validators=[DataRequired(), Length(4, 16)])
    password = StringField(_l('Password'))
    email = StringField(_l('Email'), validators=[DataRequired(), Email(),Length(7, 31)])
    group = QuerySelectField(_l('User Group'), query_factory=userGroup_db.getAlluserGroup, get_label="name")
    submit = SubmitField(_l('Submit'))


class UserRegisterForm(FlaskForm):
    id = StringField(u'Id')
    username = StringField(_l('Username'), validators=[DataRequired(), Length(4, 16)])
    password = StringField(_l('Password'),validators=[DataRequired(), Length(5, 16)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(),Length(7, 31)])
    group = QuerySelectField(_l('User Group'), query_factory=userGroup_db.getAlluserGroup, get_label="name")
    submit = SubmitField(_l('New User'))


class PageDownForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(),Length(1, 64)])
    source = QuerySelectField(_l('Source'),query_factory=articleSource_db.getAll,get_label="name")
    type = QuerySelectField(_l('Type'),query_factory=articleType_db.getAll,get_label="name")
    summary = TextAreaField(_l('Summary'), validators=[DataRequired()])
    tags = StringField(_l('Tags'))
    content = PageDownField(_l("Enter MarkDown Text"),validators=[DataRequired()])
    no_clean = None
    submit = SubmitField(_l('Submit'))

class AdvancedPageDownForm(PageDownForm):
    no_clean = BooleanField(_l("Using Advanced Mode"))

class FileEditForm(FlaskForm):
    id = StringField(u'Id')
    alias = StringField(_l('Alias'), validators=[DataRequired(), Length(1, 16)])
    description = TextAreaField(_l("Description"))
    external = BooleanField(_l("External Link"),default=True)
    permission = QuerySelectField(_l("Access Permission"), query_factory=userGroup_db.getAlluserGroup, get_label="name")
    link = StringField(_l("Link"))
    password = StringField(_l("Password"))
    submit = SubmitField(_l("Update Info"))

class FileUploadForm(FileEditForm):
    submit = SubmitField(_l("New File"))

class DeleteForm(FlaskForm):
    id = StringField(u"id")
    submit = SubmitField(_l("Confirm"))
