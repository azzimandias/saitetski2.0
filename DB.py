import psycopg2

# подключение к базе данных
con = psycopg2.connect(host="127.0.0.1",
                       database="Lenin museum",
                       user="postgres",
                       password="fuckyou")

# указатель
cur = con.cursor()
c = con.cursor()
# cur.execute('select passport№, name, surname, patronymic, work_experience, function from employees')
# rows = cur.fetchall()
# for r in rows:
#     print (f"passport№: {r[0]} name: {r[1]} surname: {r[2]} patronymic: {r[3]} work_experience: {r[4]} function: {r[5]}")
# cur.close()
# закрыть подключение
# con.close()
