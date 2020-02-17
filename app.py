from flask import Flask
from flask import render_template, flash, redirect, url_for, request
import logging
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from config import Config
from forms import LoginForm, RegistrationForm, CheckForm, ExtendForm, Sub1, Sub2, Sub3, Sub4, Sub5, Sub6, Sub7, Sub8, Basket, SS
from flask_login import UserMixin
from DB import cur, con
usn = ''
a = 0
card = 0
tiktok2 = []
exhibits_list = []
dodik = ''
Surname = ''
num_ticket = []
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
    global exhibits_list, dodik, num_ticket
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
        for rec in request.form:
            if rec == 'submit1':
                num_ticket.append(0)
            if rec == 'submit1d':
                num_ticket.append(1)
            if rec == 'submit2':
                num_ticket.append(2)
            if rec == 'submit2d':
                num_ticket.append(3)
            if rec == 'submit3':
                num_ticket.append(4)
            if rec == 'submit3d':
                num_ticket.append(5)
            if rec == 'submit4':
                num_ticket.append(6)
            if rec == 'submit4d':
                num_ticket.append(7)
        sex()
    cur.execute("select * from exhibition")
    exhibitions = cur.fetchall()
    j = []
    for exx in exhibitions:
        j.append(exx[0])

    con.commit()
    cur.execute("select hall_name from hall")
    hall_name = cur.fetchall()
    i = []
    for hall in hall_name:
        i.append(hall[0])

    con.commit()
    cur.execute("select floor№ from hall")
    floor = cur.fetchall()
    f = []
    for ffloor in floor:
        f.append(ffloor[0])

    con.commit()
    cur.execute("select price from ticket")
    price = cur.fetchall()
    p = []
    for pprice in price:
        p.append(pprice[0])
    con.commit()
    return render_template('MainPage.html', exhibition1=j[0], exhibition2=j[1], exhibition3=j[2], exhibition4=j[3],
                                            hall_name1=i[0], hall_name2=i[1], hall_name3=i[2], hall_name4=i[3],
                                            floor1=f[0], floor2=f[1], floor3=f[2], floor4=f[3],
                                            price1=p[0], price1d=p[1], price2=p[2], price2d=p[3], price3=p[4], price3d=p[5], price4=p[6], price4d=p[7],
                                            f1=f1, f1d=f1d, f2=f2, f2d=f2d, f3=f3, f3d=f3d, f4=f4, f4d=f4d,
                                            Poi=Poi)


def sex():
    global num_ticket, tiktok2
    tiktok2 = []
    for num in num_ticket:
        cur.execute("select * from ticket where ticket.ticket = '{number}'".format(number=num))
        tic_inf = cur.fetchall()
        con.commit()
        for tic in tic_inf:
            inside2 = {
                'exhibition':tic[3],
                'type':tic[2],
                'price':tic[1]
            }
            tiktok2.append(inside2)
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
            cur.execute("INSERT INTO customer (login, password)"
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
    work_time = []
    if usn == '':
        return redirect(url_for('MainPage'))
    if request.method == 'POST':
        dodik = Poi.poisk.data
        recc = request.form
        mama = redir(recc)
        if mama:
            Poisk()
            return redirect(url_for('Search'))
    cur.execute("select * from card")
    userss = cur.fetchall()
    con.commit()
    cur.execute("select * from employeer")
    usersss = cur.fetchall()
    con.commit()
    for a_users in userss:
        if (a_users[4] == int(current_user.id)) and (Surname == ''):
            global tiktok2
            print(Surname)
            extend = 1
            take = take_tickets()
            if tiktok2 != []:
                proverka = 1
            if request.method == 'POST':
                dodik = Poi.poisk.data
                recc = request.form
                mama = redir(recc)
                if mama:
                    Poisk()
                    return redirect(url_for('Search'))
                for rec in request.form:
                    if rec == 'yes':
                        if tiktok2 == []:
                            flash('Корзина пуста')
                            return redirect(url_for('Profile'))
                        yyes = 1
                    if rec == 'no':
                        tiktok2 = []
                        proverka = 0
                    if rec == 'yes2':
                        print(f.CV.data)
                        if f.CV.data == a_users[3]:
                            tickets_for_customers()
                            tiktok2 = []
                            proverka = 0
                            take = take_tickets()
                            print(yyes)
                            return render_template('Profile.html', extend=extend, card=a_users[0], month=a_users[1], year=a_users[2], CVV=a_users[3], f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take, Poi=Poi, Surname=Surname)
            print(yyes)
            return render_template('Profile.html', extend=extend, card=a_users[0], month=a_users[1], year=a_users[2], CVV=a_users[3], f=f, yyes=yyes, proverka=proverka, tiktok2=tiktok2, take=take, Poi=Poi, Surname=Surname)
    for a_usersss in usersss:
        if (Surname != '') and (a_usersss[1] == current_user.username):
            form = ExtendForm()
            cur.execute("select * from employeer_in_the_hall where passport = {pas}".format(pas=a_usersss[0]))
            in_hall = cur.fetchall()
            con.commit()
            for hall in in_hall:
                inside3={
                    'date':hall[0],
                    'entry_time':hall[1],
                    'exit_time':hall[2],
                    'hall_name':hall[3],
                }
                work_time.append(inside3)
            return render_template('Profile.html', extend=extend, f=f, yyes=yyes, Poi=Poi, form=form, Surname=Surname, surname=a_usersss[3], patronymic=a_usersss[4], function=a_usersss[6], work_time=work_time)
    con.commit()
    form = ExtendForm()
    if request.method == 'POST':
        for rec in request.form:
            if rec == 'submit':
                cur.execute("INSERT INTO card (customer_id, card№, card_month, card_year, card_cvv)"
                            "VALUES ({}, {}, {}, {}, {})".format(current_user.id, form.card.data, form.month.data, form.year.data, form.CVV.data))
                con.commit()
                extend = 1
                return render_template('Profile.html', form=form, extend=extend, card=form.card.data, month=form.month.data, year=form.year.data, CVV=form.CVV.data, f=f, Poi=Poi, Surname=Surname)
            if rec == 'yes':
                yyes = 1
    return render_template('Profile.html', form=form, extend=extend, f=f, yyes=yyes, Poi=Poi, Surname=Surname)



def take_tickets():
    tics = []
    cur.execute("select * from ticket_for_customer where customer_id = {id}".format(id=int(current_user.id)))
    ticket = cur.fetchall()
    con.commit()
    for tic in ticket:
        cur.execute("select * from ticket where ticket.ticket = {num}".format(num=tic[2]))
        t = cur.fetchall()
        con.commit()
        for path in t:
            inside={
                'ticket':tic[0],
                'exhibition':path[3],
                'type':path[2],
                'price':path[1]
            }
            tics.append(inside)
    return tics


def tickets_for_customers():
    global num_ticket
    for num in num_ticket:
        cur.execute("INSERT INTO ticket_for_customer (customer_id, ticket)"
                    "VALUES ({}, {})".format(int(current_user.id), num))
        con.commit()
    num_ticket = []



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
        cur.execute("select * from customer")
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
    global a, Surname
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
        cur.execute("select * from customer")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                usn = a_user[1]
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('Profile'))
        con.commit()
        a = 2
        cur.execute("select * from employeer")
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                usn = a_user[1]
                Surname = a_user[3]
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('Profile'))
    return render_template('SingIn.html', title='Sign In', form=form, Poi=Poi)


@app.route('/Logout')
def Logout():
    global tiktok2, Surname, num_ticket
    Surname = ''
    tiktok2 = []
    num_ticket = []
    logout_user()
    return redirect(url_for('MainPage'))


@app.route('/logout')
def logout():
    global tiktok2, Surname, num_ticket
    Surname = ''
    tiktok2 = []
    num_ticket = []
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
    cur.execute("select * from exhibit where exhibit_name like '%{dodik}%'".format(dodik=dodik))
    all_info = cur.fetchall()
    con.commit()
    print(all_info)
    global exhibits_list
    exhibits_list = []
    if dodik == '':
        return exhibits_list
    for singl_info in all_info:
        id = singl_info[4]
        cur.execute("select distinct exposition_name from exposition where exposition_inventory = '{id}'".format(id=id))
        expo = cur.fetchall()
        con.commit()
        for ex in expo:
            inf = {
                'exhibit_name':singl_info[1],
                'view_name':singl_info[6],
                'type_name':singl_info[5],
                'exposition_name':ex[0],
                'exhibition_name':singl_info[3],
                'hall_name':singl_info[2],
            }
            exhibits_list.append(inf)
    return exhibits_list

