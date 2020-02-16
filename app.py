from flask import Flask
from flask import render_template, flash, redirect, url_for, request
import logging
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from config import Config
from forms import LoginForm, RegistrationForm, CheckForm, ExtendForm, Sub1, Sub2, Sub3, Sub4, Sub5, Sub6, Sub7, Sub8, Basket, SS
from flask_login import UserMixin
#from __init__ import login
from DB import cur, con
usn = ''
a = 0
passworld = ''
card = 0
tiktok2 = []
exhibits_list = []
dodik = ''
Surname = ''
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
            self.username = usn
            con.commit()
        elif a == 2:
            self.username = usn
            con.commit()


# Routes ######################################################################
@app.route('/', methods=['GET', 'POST'])
def MainPage():
    global exhibits_list, dodik
    cur.execute("set lc_monetary to 'Russian_Russia.UTF-8'")
    con.commit()
    Poi = SS()
    f1 = Sub1()
    f1d = Sub2()
    f2 = Sub3()
    f2d = Sub4()
    f3 = Sub5()
    f3d = Sub6()
    f4 = Sub7()
    f4d = Sub8()
    if (request.method == 'POST'):
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
        s = 0
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
        sex(s)
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
                                            f1=f1, f1d=f1d, f2=f2, f2d=f2d, f3=f3, f3d=f3d, f4=f4, f4d=f4d,
                                            Poi=Poi)


def sex(s):
    t=[]
    exhibition = ''
    type = ''
    price = ''
    cur.execute("select distinct price from tickets")
    tic = cur.fetchall()
    for ttic in tic:
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
    inside2 = {
        'exhibition':exhibition,
        'type':type,
        'price':price
    }
    tiktok2.append(inside2)
    print(tiktok2)
    return tiktok2


@app.route('/SingUp', methods=['GET', 'POST'])
def SingUp():
    global dodik
    Poi = SS()
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    reg_form = RegistrationForm()
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
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
    return render_template('SingUp.html', form=reg_form, Poi=Poi)


@app.route('/Profile', methods=['GET', 'POST'])
def Profile():
    global dodik, Surname
    Poi = SS()
    f = Basket()
    yyes = 0
    extend = 0
    proverka = 0
    if usn == '':
        return redirect(url_for('MainPage'))
    user = current_user.username
    cur.execute("select * from cards")
    userss = cur.fetchall()
    con.commit()
    cur.execute("select * from employees")
    usersss = cur.fetchall()
    for a_users in userss:
        print(a_users)
        if (a_users[1] == user) and (Surname == ''):
            global tiktok2
            print(Surname)
            extend = 1
            con.commit()
            card = a_users[3]
            month = a_users[4]
            year = a_users[5]
            CVV = a_users[6]
            con.commit()
            take = take_tickets()
            if tiktok2 != []:
                proverka = 1
                print(tiktok2)
                tt = []
                ttt = []
                i = 0
                for tik in tiktok2:
                    print(tik)
                    for tok in tik:
                        tt.append(tok)
                    ttt.append(tt)
                print(ttt)
            if request.method == 'POST':
                dodik = Poi.poisk.data
                recc = request.form
                mama = redir(recc)
                if mama:
                    Poisk()
                    return redirect(url_for('Search'))
                card = a_users[3]
                month = a_users[4]
                year = a_users[5]
                CVV = a_users[6]
                for rec in request.form:
                    if rec == 'yes':
                        if tiktok2 == []:
                            break
                        yyes = 1
                    if rec == 'no':
                        tiktok2 = []
                        proverka = 0
                    if rec == 'yes2':
                        print(f.CVV.data)
                        if f.CVV.data == CVV:
                            tickets_for_customers()
                            tiktok2 = []
                            proverka = 0
                            take = take_tickets()
                            return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take, Poi=Poi, Surname=Surname)
            return render_template('Profile.html', extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take, Poi=Poi, Surname=Surname)
    for a_usersss in usersss:
        if (a_usersss[1] == user) and (Surname != ''):
            form = ExtendForm()
            return render_template('Profile.html', extend=extend, f=f, yyes=yyes, Poi=Poi, form=form, Surname=Surname)
    con.commit()
    form = ExtendForm()
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
        for rec in request.form:
            if rec == 'submit':
                card = form.card.data
                month = form.month.data
                year = form.year.data
                CVV = form.CVV.data
                cur.execute("INSERT INTO cards (id, login, password, card№, card_month, card_year, card_cvv)"
                            "VALUES ({}, '{}', '{}', {}, {}, {}, {})".format(current_user.id, current_user.username, passworld, card, month, year, CVV))
                con.commit()
                extend = 1
                return render_template('Profile.html', form=form, extend=extend, card=card, month=month, year=year, CVV=CVV, f=f, Poi=Poi)
            if rec == 'yes':
                yyes = 1
    return render_template('Profile.html', form=form, extend=extend, f=f, yyes=yyes, Poi=Poi)



def take_tickets():
    cur.execute("select * from tickets_for_customers")
    tic = cur.fetchall()
    vivod = []
    for t in tic:
        print(t[1])
        if t[1] == current_user.username:
            list = {
                'tic':t[7],
                'exhib':t[3],
                'typ':t[4],
                'pric':t[6]
            }
            vivod.append(list)
    con.commit()
    return vivod


def tickets_for_customers():
    for ticket in tiktok2:
        print(ticket['exhibition'])
        print(ticket['type'])
        print(ticket['price'])
        cur.execute("INSERT INTO tickets_for_customers (id, login, password, exhibition_name, ttype_name, price)"
                    "VALUES ({}, '{}', '{}', '{}', '{}', '{}')".format(current_user.id, current_user.username, passworld, ticket['exhibition'], ticket['type'], ticket['price']))
        con.commit()



@app.route('/Loh', methods=['GET', 'POST'])
def Loh():
    global dodik
    Poi = SS()
    pas = ''
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    form = CheckForm()
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
    if form.validate_on_submit():
        username = form.username.data
        cur.execute("select * from customers")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username:
                pas = a_user[2]
    return render_template('Loh.html', form=form, pas=pas, Poi=Poi)


@app.errorhandler(404)
def Fourzerofour(e):
    Poi = SS()
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
    return render_template('ErrorPage.html', Poi=Poi), 404


@app.route('/SingIn', methods=['GET', 'POST'])
def SingIn():
    Poi = SS()
    global a, passworld, Surname
    global usn, dodik
    if a == 0:
        logout()
    if current_user.is_authenticated:
        return redirect(url_for('MainPage'))
    form = LoginForm()
    a = 1
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
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
        cur.execute("select * from employees")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                usn = a_user[1]
                Surname = a_user[3]
                login_user(user, remember=form.remember_me.data)
                passworld = password
                return redirect(url_for('Profile'))
    return render_template('SingIn.html', title='Sign In', form=form, Poi=Poi)


@app.route('/Logout')
def Logout():
    global tiktok2, Surname
    Surname = ''
    tiktok2 = []
    logout_user()
    return redirect(url_for('MainPage'))


@app.route('/logout')
def logout():
    global tiktok2, Surname
    Surname = ''
    tiktok2 = []
    logout_user()
    return redirect(url_for('SingIn'))


@app.route('/Search', methods=['GET', 'POST'])
def Search():
    global exhibits_list, dodik
    Poi = SS()
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        redir(recc)
        Poisk()
    return render_template('Search.html', Poi=Poi, exhibits_list=exhibits_list, dodik=dodik)


def redir(recc):
    mama = 0
    for rec in recc:
        if rec == 'sub':
            mama = 1
    return mama


def Poisk():
    global dodik
    print(dodik)
    cur.execute("select * from exhibits where exhibit_name like '%{dodik}%'".format(dodik=dodik))
    all_info = cur.fetchall()
    con.commit()
    print(all_info)
    global exhibits_list
    exhibits_list = []
    if dodik == '':
        return exhibits_list
    for singl_info in all_info:
        inf = {
            'exhibit_name':singl_info[9],
            'view_name':singl_info[7],
            'type_name':singl_info[5],
            'exposition_name':singl_info[2],
            'exhibition_name':singl_info[0],
            'hall_name':singl_info[3],
        }
        exhibits_list.append(inf)
    return exhibits_list

