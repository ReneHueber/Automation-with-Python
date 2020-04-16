from pynput import keyboard
import threading
import time
from datetime import datetime
from keyLogger import DbConnection

db_path = "/home/ich/Database/Keylogger/KeyStrokes.db"


# class for the date an the key strokes
class KeyLog:
    date = None
    keystrokes = None


key_log = KeyLog()


# counts all the keystrokes, but not the key values
def on_release(key):
    key_log.keystrokes += 1
    print(key_log.keystrokes)


# set's up the database and get's the value for the current day is existing
def setup_db():
    # get's the current date for the db entrance
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    key_log.date = str(date)

    # sql command to create the table
    create_table_sql = """CREATE TABLE IF NOT EXISTS KeyLogs (
                    id integer PRIMARY KEY,
                    date Date NOT NULL,
                    keystrokes integer NOT NULL);"""

    # connects and creates the table
    conn = DbConnection.create_connection(db_path)

    if conn is not None:
        DbConnection.create_table(conn, create_table_sql)

        # get's the values for the keystrokes at this day, is there are no for today, an entrance is created
        with conn:
            keystrokes = DbConnection.select_by_date(conn, key_log.date)
            if keystrokes is not None:
                key_log.keystrokes = keystrokes
            else:
                key_log.keystrokes = 0
                DbConnection.create_entrance(conn, (key_log.date, key_log.keystrokes))

        # closes the connection the the database
        DbConnection.close_connection(conn)
    else:
        print("No connection to the database!")


def update_db():
    while True:
        conn = DbConnection.create_connection(db_path)
        with conn:
            DbConnection.update_value_by_date(conn, (key_log.keystrokes, key_log.date))
        time.sleep(10)


# setup of the global key listener
def setup_key_listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


# starting the threads
if __name__ == "__main__":
    print("Key Logger started")
    setup_db()
    t1 = threading.Thread(target=update_db)
    t2 = threading.Thread(target=setup_key_listener)
    t1.start()
    t2.start()

