from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from DB import cur, con


class LoginForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('OK!')

class CheckForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    submit = SubmitField('OK!')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Пожалуйста, возьмите мои данные и пользуйтесь ими в ваших личных целях')

    def validate_username(self, username):
        cur.execute("SELECT login FROM customers")
        loginList = cur.fetchall()
        for login in loginList:
            if username.data == login[0]:
                raise ValidationError('Это имя пользователя занято, придумайте другое.')
                raise ValidationError('Please use a different username.')
