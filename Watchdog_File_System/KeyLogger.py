from timeloop import Timeloop
from datetime import timedelta
from pynput import keyboard

keyLogs = {}
t1 = Timeloop()


def on_release(key):
    try:
        if key.char in keyLogs:
            keyLogs[key.char] += 1
        else:
            keyLogs[key.char] = 1
    except AttributeError:
        str_key = "{0}".format(key)
        key_value = str_key.split(".")[1]

        if key_value == "None":
            key_value = "alt_gr"

        if key_value in keyLogs:
            keyLogs[key_value] += 1
        else:
            keyLogs[key_value] = 1


@t1.job(interval=timedelta(seconds=2))
def write_file():
    print(keyLogs)


t1.start(block=True)


with keyboard.Listener(on_release=on_release) as listener:
    listener.join()



