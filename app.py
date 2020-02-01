from flask import Flask
from flask import render_template, flash, redirect, url_for, request
import logging
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from config import Config
from forms import LoginForm, RegistrationForm, CheckForm, ExtendForm
from flask_login import UserMixin
#from __init__ import login
from DB import cur, con
global usn
usn = ''
global a
a = 0
global passworld
passworld = ''

# Run ######################################################################
app = Flask(__name__)

app.config.from_object(Config)

if __name__ == '__main__':
    app.run()

# User Model for Flask-Login ######################################################################
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User(user_id)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.set_username()

    def set_username(self):
        if a == 1:
            # cur.execute("select login from customers")
            # username = cur.fetchone()
            self.username = usn  # username[0]
            con.commit()
        elif a == 2:
            # cur.execute("select name from employees")
            # username = cur.fetchone()
            self.username = usn # username[0]
            con.commit()


# Routes ######################################################################
@app.route('/')
def MainPage():
    return render_template('MainPage.html')#, login=login)


@app.route('/SingUp', methods=['GET', 'POST'])
def SingUp():
    #return render_template('SingUp.html')
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        print('form.register succeed')
        try:
            cur.execute("INSERT INTO customers (login, password)"
                        "VALUES ('{}', '{}')".format(reg_form.username.data, reg_form.password.data))
            con.commit()
        except:
            logging.exception('')
            print('user not registered')
            cur.execute("ROLLBACK")
            con.commit()
        return redirect(url_for('SingIn'))
    return render_template('SingUp.html', form=reg_form)


@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    card = 0
    month = 0
    year = 0
    CVV = 0
    extend = 0
    if usn == '':
        return redirect(url_for('MainPage'))
    user = current_user.username
    cur.execute("select * from cards")
    userss = cur.fetchall()
    for a_users in userss:
        print(a_users)
        if a_users[1] == user:
            extend = 1
            con.commit()
            card = a_users[3]
            month = a_users[4]
            year = a_users[5]
            CVV = a_users[6]
            return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV)
    con.commit()
    form = ExtendForm()
    if request.method == 'POST':
        card = form.card.data
        month = form.month.data
        year = form.year.data
        CVV = form.CVV.data
        try:
            cur.execute("INSERT INTO cards (id, login, password, card№, card_month, card_year, card_cvv)"
                    "VALUES ({}, '{}', '{}', {}, {}, {}, {})".format(current_user.id, current_user.username, passworld, card, month, year, CVV))
            con.commit()
            extend = 1
        except:
            logging.exception('')
            print('wrong')
            cur.execute("ROLLBACK")
            con.commit()
    return render_template('Profile.html', form=form, extend=extend)


@app.route('/Loh', methods=['GET', 'POST'])
def Loh():
    pas = ''
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    form = CheckForm()
    if form.validate_on_submit():
        username = form.username.data
        cur.execute("select * from customers")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username:
                pas = a_user[2]
    return render_template('Loh.html', form=form, pas=pas)


@app.errorhandler(404)
def Fourzerofour(e):
    return render_template('ErrorPage.html'), 404


@app.route('/SingIn', methods=['GET', 'POST'])
def SingIn():
    global a, passworld
    global usn
    if a == 0:
        logout()
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    form = LoginForm()
    a = 1
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur.execute("select * from customers")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                usn = a_user[1]
                login_user(user, remember=form.remember_me.data)
                passworld = password
                return redirect(url_for('Profile'))
        con.commit()
        a = 2
        cur.execute("select passport№, name, password from employees")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                usn = a_user[1]
                login_user(user, remember=form.remember_me.data)
                passworld = password
                return redirect(url_for('Profile'))
    return render_template('SingIn.html', title='Sign In', form=form)


@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('MainPage'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('SingIn'))
