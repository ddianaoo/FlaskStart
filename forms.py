from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Your Username: ', validators=[Length(min=4, max=20)])
    email = EmailField('Your email: ', validators=[Email()])
    password = PasswordField('Your password: ', validators=[DataRequired(), Length(min=4, max=20)])
    remember = BooleanField('Remain me', default=False)
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Your Username: ', validators=[Length(min=4, max=20)])
    email = EmailField('Your email: ', validators=[Email()])
    password = PasswordField('Your password: ', validators=[DataRequired(), Length(min=4, max=20)])
    password2 = PasswordField('Your password2: ', validators=[DataRequired(), Length(min=4, max=20), EqualTo('password')])
    submit = SubmitField('Send')


class ContactForm(FlaskForm):
    username = StringField('Your Username: ', validators=[Length(min=4, max=20)])
    email = EmailField('Your email: ', validators=[Email()])
    message = TextAreaField('Your message: ')
    submit = SubmitField('Send')


class AddPostForm(FlaskForm):
    title = StringField('Title: ')
    url = StringField('Slag: ')
    text = TextAreaField('Text: ')
    submit = SubmitField('Add')