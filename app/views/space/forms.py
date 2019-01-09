from flask_wtf import Form,FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields import StringField,TextAreaField,SubmitField,PasswordField,BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Length,EqualTo,Email

from ...model.mysql.blog import articleType_db,articleSource_db

from . import space
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

class DeleteForm(FlaskForm):
    submit = SubmitField(u"Delete")


class ProfileEditForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(), Length(4, 16)])
    email = StringField(u'Email', validators=[DataRequired(), Email(),Length(7, 31)])
    submit = SubmitField(u'更新资料')

class ChangePasswordForm(FlaskForm):
    password = PasswordField(u'Password', validators=[DataRequired(), Length(6, 16),EqualTo("confirm")])
    confirm= PasswordField(u'Password', validators=[DataRequired(), Length(6, 16)])
    submit = SubmitField(u'Submit')
