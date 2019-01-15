from flask_wtf import Form,FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms.fields import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), Length(4, 16)])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(6, 16)])
    submit = SubmitField(_l('Login'))