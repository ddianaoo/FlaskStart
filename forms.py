from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField
from wtforms.validators import Email, Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField('Your Username: ')
    email = EmailField('Your email: ', validators=[Email()])
    password = PasswordField('Your password: ', validators=[DataRequired(), Length(min=4, max=20)])
    remember = BooleanField('Remain me', default=False)
    submit = SubmitField('Log in')
