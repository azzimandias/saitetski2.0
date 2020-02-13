from flask import Flask
from flask import render_template, flash, redirect, url_for, request
import logging
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from config import Config
from forms import LoginForm, RegistrationForm, CheckForm, ExtendForm, Sub1, Sub2, Sub3, Sub4, Sub5, Sub6, Sub7, Sub8, Basket
from flask_login import UserMixin
#from __init__ import login
from DB import cur, con
global usn
usn = ''
global a
a = 0
global passworld
passworld = ''
global card
card = 0
global tiktok
tiktok = []
global tiktok2
tiktok2 = []
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
@app.route('/', methods=['GET', 'POST'])
def MainPage():
    f1 = Sub1()
    f1d = Sub2()
    f2 = Sub3()
    f2d = Sub4()
    f3 = Sub5()
    f3d = Sub6()
    f4 = Sub7()
    f4d = Sub8()
    if (request.method == 'POST'):
        s = 0
        # print(request.form)
        for rec in request.form:
            if rec == 'submit1':
                s = 1
            if rec == 'submit1d':
                s = 2
            if rec == 'submit2':
                s = 3
            if rec == 'submit2d':
                s = 4
            if rec == 'submit3':
                s = 5
            if rec == 'submit3d':
                s = 6
            if rec == 'submit4':
                s = 7
            if rec == 'submit4d':
                s = 8
        bor = []
        bor = sex(s)
        print(tiktok)
        print(tiktok[0])
    cur.execute("select distinct * from exhibitions")
    exhibitions = cur.fetchall()
    j = []
    for exx in exhibitions:
        j.append(exx[0])

    con.commit()
    cur.execute("select distinct hall_name from hall")
    hall_name = cur.fetchall()
    i = []
    for hall in hall_name:
        i.append(hall[0])

    con.commit()
    cur.execute("select distinct floor№ from hall")
    floor = cur.fetchall()
    f = []
    for ffloor in floor:
        f.append(ffloor[0])

    con.commit()
    cur.execute("select distinct price from tickets")
    price = cur.fetchall()
    p = []
    for pprice in price:
        p.append(pprice[0])
    con.commit()
    return render_template('MainPage.html', exhibition1=j[0], exhibition2=j[1], exhibition3=j[2], exhibition4=j[3],
                                            hall_name1=i[0], hall_name2=i[1], hall_name3=i[2], hall_name4=i[3],
                                            floor1=f[0], floor2=f[1], floor3=f[2], floor4=f[3],
                                            price1=p[1], price1d=p[0], price2=p[3], price2d=p[2], price3=p[5], price3d=p[4], price4=p[7], price4d=p[6],
                                            f1=f1, f1d=f1d, f2=f2, f2d=f2d, f3=f3, f3d=f3d, f4=f4, f4d=f4d)


def sex(s):
    t=[]
    cur.execute("select distinct price from tickets")
    tic = cur.fetchall()
    for ttic in tic:
        # t.append(ttic[0])
        for tttic in ttic:
            print(tttic)
            t.append(tttic)
    if s == 2:
        price = t[0]
    elif s == 1:
        price = t[1]
    elif s == 4:
        price = t[2]
    elif s == 3:
        price = t[3]
    elif s == 6:
        price = t[4]
    elif s == 5:
        price = t[5]
    elif s == 8:
        price = t[6]
    elif s == 7:
        price = t[7]
    con.commit()
    ty = []
    cur.execute("select distinct ttype_name from tickets_types")
    typ = cur.fetchall()
    for ttyp in typ:
        # ty.append(ttyp[0])
        for tttyp in ttyp:
            ty.append(tttyp)
    if s == 2:
        type = ty[0]
    if s == 1:
        type = ty[1]
    if s == 4:
        type = ty[0]
    if s == 3:
        type = ty[1]
    if s == 6:
        type = ty[0]
    if s == 5:
        type = ty[1]
    if s == 8:
        type = ty[0]
    if s == 7:
        type = ty[1]
    con.commit()
    ex = []
    cur.execute("select distinct * from exhibitions")
    exh = cur.fetchall()
    for eexh in exh:
        # ex.append(eexh[0])
        for eeexh in eexh:
            ex.append(eeexh)
    if s == 2:
        exhibition = ex[0]
    if s == 1:
        exhibition = ex[0]
    if s == 4:
        exhibition = ex[1]
    if s == 3:
        exhibition = ex[1]
    if s == 6:
        exhibition = ex[2]
    if s == 5:
        exhibition = ex[2]
    if s == 8:
        exhibition = ex[3]
    if s == 7:
        exhibition = ex[3]
    con.commit()
    # ticket = []
    inside = [exhibition,type,price]
    inside2 = {
        'exhibition':exhibition,
        'type':type,
        'price':price
    }
    tiktok.append(inside)
    tiktok2.append(inside2)
    print(tiktok)
    print(tiktok2)
    return tiktok


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
    f = Basket()
    yyes = 0
    card = 0
    month = 0
    year = 0
    CVV = 0
    extend = 0
    # extend = 1
    proverka = 0
    # proverka = 1
    if usn == '':
        return redirect(url_for('MainPage'))
    user = current_user.username
    cur.execute("select * from cards")
    userss = cur.fetchall()
    for a_users in userss:
        print(a_users)
        if a_users[1] == user:
            global tiktok
            global tiktok2
            extend = 1
            con.commit()
            card = a_users[3]
            month = a_users[4]
            year = a_users[5]
            CVV = a_users[6]
            con.commit()
            take = []
            take = take_tickets()
            if tiktok != []:
                proverka = 1
                print(tiktok)
                first=[]
                second=[]
                third=[]
                tt = []
                ttt = []
                i = 0
                for tik in tiktok:
                    print(tik)
                    first=[]
                    second=[]
                    third=[]
                    tt = []
                    for tok in tik:
                        if i == 2:
                            third.append(tok)
                            i=0
                            break
                        if i == 1:
                            second.append(tok)
                            i+=1
                        if i == 0:
                            first.append(tok)
                            i+=1
                    tt.append(first)
                    tt.append(second)
                    tt.append(third)
                    ttt.append(tt)
                print(ttt)
            if request.method == 'POST':
                for rec in request.form:
                    if rec == 'yes':
                        if tiktok == []:
                            break
                        yyes = 1
                    if rec == 'no':
                        tiktok = []
                        tiktok2 = []
                        proverka = 0
                    if rec == 'yes2':
                        print(f.CVV.data)
                        if f.CVV.data == CVV:
                            tickets_for_customers(ttt)
                            tiktok = []
                            tiktok2 = []
                            proverka = 0
                            take = take_tickets()
                            return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take)
            return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take)
    con.commit()
    form = ExtendForm()
    if request.method == 'POST':
        for rec in request.form:
            if rec == 'submit':
                card = form.card.data
                month = form.month.data
                year = form.year.data
                CVV = form.CVV.data
                try:
                    cur.execute("INSERT INTO cards (id, login, password, card№, card_month, card_year, card_cvv)"
                            "VALUES ({}, '{}', '{}', {}, {}, {}, {})".format(current_user.id, current_user.username, passworld, card, month, year, CVV))
                    con.commit()
                    extend = 1
                    return render_template('Profile.html', form=form, extend=extend, card=card, month=month, year=year, CVV=CVV)
                except:
                    logging.exception('')
                    print('wrong')
                    cur.execute("ROLLBACK")
                    con.commit()
            if rec == 'yes':
                yyes = 1
    return render_template('Profile.html', form=form, extend=extend, f=f, yyes=yyes)
    # return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, proverka=proverka, tiktok2=tiktok2)


def take_tickets():
    cur.execute("select * from tickets_for_customers")
    tic = cur.fetchall()
    vivod = []
    for t in tic:
        print(t[1])
        if t[1] == current_user.username:
            list = {
                'exhib':t[3],
                'typ':t[4],
                'pric':t[6]
            }
            vivod.append(list)
    con.commit()
    return vivod


def tickets_for_customers(ttt):
    print(ttt)
    i = 0
    fir=''
    sec=''
    thr=''
    for ticket in ttt:
        for t in ticket:
            for ti in t:
                if i == 2:
                    thr=ti
                    i=0
                    break
                if i == 1:
                    sec=ti
                    i+=1
                if i == 0:
                    fir=ti
                    i+=1
        try:
            cur.execute("INSERT INTO tickets_for_customers (id, login, password, exhibition_name, ttype_name, price)"
                        "VALUES ({}, '{}', '{}', '{}', '{}', '{}')".format(current_user.id, current_user.username, passworld, fir, sec, thr))
            con.commit()
        except:
            logging.exception('')
            print('wrong')
            cur.execute("ROLLBACK")
            con.commit()
        fir=''
        sec=''
        thr=''


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
    global tiktok
    global tiktok2
    tiktok = []
    tiktok2 = []
    logout_user()
    return redirect(url_for('MainPage'))


@app.route('/logout')
def logout():
    global tiktok
    global tiktok2
    tiktok = []
    tiktok2 = []
    logout_user()
    return redirect(url_for('SingIn'))

@app.route('/Search')
def Seach():
    return render_template('Search.html')
