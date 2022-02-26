from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
from app.models import User


class RegistraionForm(FlaskForm):
    def user_validate(self, username):
        name = User.query.filter_by(username=username.data).first()
        if name:
            raise ValidationError("Username already exists.")
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], label='username')
    email = StringField(validators=[InputRequired(), Length(min=4, max=30), Email()], label='email')
    pass1 = PasswordField(validators=[InputRequired(), Length(min=6)], label='password1')
    pass2 = PasswordField(validators=[InputRequired(), Length(min=6), EqualTo("pass1")], label='password2')
    submit = SubmitField(label='submit')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], label='username')
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], label='password')
    submit = SubmitField(label='submit')
