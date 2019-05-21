from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from flask_pagedown.fields import PageDownField
from wtforms.fields import StringField,TextAreaField,SubmitField,PasswordField,BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from app.mysql import articleType_db,articleSource_db

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

class DeleteForm(FlaskForm):
    submit = SubmitField(_l("Confirm"))


class ProfileEditForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(4, 16)])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(),Length(7, 31)])
    submit = SubmitField(_l('Update Info'))

class ChangePasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(6, 16),EqualTo("confirm")])
    confirm= PasswordField(_l('ConfirmedPassword'), validators=[DataRequired(), Length(6, 16)])
    submit = SubmitField(u'Submit')
