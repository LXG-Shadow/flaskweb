from flask_wtf import Form,FlaskForm
from wtforms.fields import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired(), Length(4, 16)])
    password = PasswordField(u'Password', validators=[DataRequired(), Length(6, 16)])
    submit = SubmitField(u'登陆')