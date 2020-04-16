import sqlite3
from sqlite3 import Error

db_file_path = '/home/ich/Database/Keylogger/Test.db'

sql_create_clicks_table = """ CREATE TABLE IF NOT EXISTS clicks (
                                id integer PRIMARY KEY,
                                date DATE NOT NULL,
                                clicks integer NOT NULL);"""


# creates the connection to the database
def create_connection(db_file):
    c = None
    try:
        c = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return c


# creates the table, if it is not existing
def create_table(c, table_sql):
    try:
        c = c.cursor()
        c.execute(table_sql)
    except Error as e:
        print(e)


# creates a new entrance in the database
def create_entrance(c, click_values):

    sql = ''' INSERT INTO clicks(date, clicks) VALUES(?,?) '''

    cur = c.cursor()
    cur.execute(sql, click_values)
    return cur.lastrowid


# updates the entrance
def update_clicks(c, click_values):

    sql = ''' UPDATE clicks SET clicks = ? WHERE date = ?'''

    cur = c.cursor()
    cur.execute(sql, click_values)
    c.commit()


# get's all the values saved in the database
def select_values(c):

    cur = c.cursor()
    cur.execute("SELECT * FROM clicks")

    rows = cur.fetchall()
    total = 0

    for row in rows:
        print(row)
        total += row[2]

    print(total)


conn = create_connection(db_file_path)

if conn is not None:
    create_table(conn, sql_create_clicks_table)

    with conn:
        values = ("2020-04-15", 6000)
        create_entrance(conn, values)
else:
    print("Error! cannot create the database connection.")
