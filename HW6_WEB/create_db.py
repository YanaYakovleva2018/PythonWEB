import sqlite3

def create_db():
    with open('create_tables.sql', 'r') as fl:
        sql = fl.read()


    with sqlite3.connect('university.db') as connect:
        cur = connect.cursor()
        cur.executescript(sql)

if __name__ == "__main__":
    create_db()