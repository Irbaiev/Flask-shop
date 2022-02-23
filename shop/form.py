import email
from logging.config import valid_ident
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import email_validator 
from shop.models import User
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('This field is required!'),  Email("Invalid email!")])
    password = PasswordField('Пароль', validators=[DataRequired('This field is required!')])
    confirm_password = PasswordField ('Подтвердите пароль',validators=[DataRequired('This field is required!'), EqualTo('password')])
    submit = SubmitField('Регистрация')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email exists')