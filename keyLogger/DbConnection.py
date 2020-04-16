import sqlite3
from sqlite3 import Error


# creates the connection to the database
def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# creates the table if is not existing;
def create_table(conn, table_sql):

    try:
        c = conn.cursor()
        c.execute(table_sql)
    except Error as e:
        print(e)


# closes the connection
def close_connection(conn):
    conn.close()


# get's values from the db, searches for the values with a certain date
def select_by_date(conn, search_date):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM KeyLogs WHERE date=?", (search_date,))

        values = c.fetchall()
        return values[0][2]
    except Error and IndexError as e:
        print(e)
        return None


# creates a new entrance for the date an keystrokes
def create_entrance(conn, values):
    sql_entrance = '''INSERT INTO KeyLogs(date, keystrokes) VALUES (?, ?)'''
    cur = conn.cursor()
    cur.execute(sql_entrance, values)
    return cur.lastrowid


# updates the value at a certain date
def update_value_by_date(conn, values):
    cur = conn.cursor()
    cur.execute("UPDATE KeyLogs SET keystrokes = ? WHERE date = ?", values)
    conn.commit()
