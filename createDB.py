"""
создаем базу данных в postgresql с названием ygolek
"""
import psycopg2

conn = psycopg2.connect(user="postgres",
        password="ghbdtnsql",
        host="127.0.0.1",
        port="5432",
        database="test_db")

conn.autocommit = True

cur = conn.cursor()

cur.execute("CREATE DATABASE ygolek")

cur.close()
conn.close()

