from flask import Flask
from flask import render_template, flash, redirect, url_for, request
import logging
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from config import Config
from forms import LoginForm
from flask_login import UserMixin
#from __init__ import login
from DB import cur, con

global a
a = 0

# form = LoginForm()
# username = form.username.data
# password = form.password.data
# cur.execute("select * from customers")
# users = cur.fetchall()
# for a_user in users:
#     print(a_user)
#     if a_user[1] == username and a_user[2] == password:
#         a = 0
#     else:
#         a = 1
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
        if a == 0:
            cur.execute("select login from customers")
            username = cur.fetchone()
            self.username = username[0]
            con.commit()
        else:
            cur.execute("select name from employees")
            username = cur.fetchone()
            self.username = username[0]
            con.commit()

# Routes ######################################################################
@app.route('/')
def MainPage():
    return render_template('MainPage.html')#, login=login)


@app.route('/SingUp')
def SingUp():
    return render_template('SingUp.html')


@app.route('/Profile')
# @login_required
def Profile():
    name = 'Andrew'
    return render_template('Profile.html', Name=name)


@app.route('/Loh')
def Loh():
    return render_template('Loh.html')


@app.errorhandler(404)
def Fourzerofour(e):
    return render_template('ErrorPage.html'), 404


@app.route('/SingIn', methods=['GET', 'POST'])
def SingIn():
    global a
    a = 0
    if current_user.is_authenticated:
        return redirect(url_for('Profile'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur.execute("select * from customers")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('Profile'))
        con.commit()
        a = 1
        cur.execute("select passport№, name, password from employees")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('Profile'))
    return render_template('SingIn.html', title='Sign In', form=form)


@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('MainPage'))
