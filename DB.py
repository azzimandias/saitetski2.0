import psycopg2

# подключение к базе данных
con = psycopg2.connect(host="127.0.0.1",
                       database="Lenin Museum",
                       user="postgres",
                       password="fuckyou")

# указатель
cur = con.cursor()
c = con.cursor()
