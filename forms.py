from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from DB import cur, con


class LoginForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('OK!')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Пожалуйста, возьмите мои данные и пользуйтесь ими в ваших личных целях')


class CheckForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    submit = SubmitField('OK!')


class ExtendForm(FlaskForm):
    card = IntegerField('5500 0000 0000 0000', validators=[DataRequired()])
    month = IntegerField('mon', validators=[DataRequired()])
    year = IntegerField('year', validators=[DataRequired()])
    CVV = IntegerField('CVV', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class Sub1(FlaskForm):
    submit1 = SubmitField('Добавить в корзину')
class Sub2(FlaskForm):
    submit1d = SubmitField('Добавить в корзину')
class Sub3(FlaskForm):
    submit2 = SubmitField('Добавить в корзину')
class Sub4(FlaskForm):
    submit2d = SubmitField('Добавить в корзину')
class Sub5(FlaskForm):
    submit3 = SubmitField('Добавить в корзину')
class Sub6(FlaskForm):
    submit3d = SubmitField('Добавить в корзину')
class Sub7(FlaskForm):
    submit4 = SubmitField('Добавить в корзину')
class Sub8(FlaskForm):
    submit4d = SubmitField('Добавить в корзину')

class Basket(FlaskForm):
    yes = SubmitField('Купить')
    no = SubmitField('Очистить корзину')
    CVV = IntegerField('Введите CVV карты', validators=[DataRequired()])
    yes2 = SubmitField('Подтвердить')

    def validate_username(self, username):
        cur.execute("SELECT login FROM customers")
        loginList = cur.fetchall()
        for login in loginList:
            if username.data == login[0]:
                raise ValidationError('Это имя пользователя занято, придумайте другое.')
                raise ValidationError('Please use a different username.')

