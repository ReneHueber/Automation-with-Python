from pynput import keyboard
import threading
import time
import os

new_key_logs = {}
file_path = "/home/ich/Shared_Data/Files/KeyLogger/KeyLogger.txt"


# register all the key strokes and saves the values to an dict
def on_release(key):
    try:
        char = key.char
        if key.vk == 65027:
            char = "alt gr"

        if char in new_key_logs:
            new_key_logs[char] += 1
        else:
            new_key_logs[char] = 1
    except AttributeError:
        str_key = "{0}".format(key)
        key_value = str_key.split(".")[1]

        if key_value == "None":
            key_value = "alt_gr"

        if key_value in new_key_logs:
            new_key_logs[key_value] += 1
        else:
            new_key_logs[key_value] = 1


# read the saved key logs
def read_saved_logs():
    saved_key_logs = {}
    # read file
    with open(file_path, "r") as key_log_file:
        for line in key_log_file:
            if line != "\n" or line != "":
                values = line.split(":")
                saved_key_logs[values[0]] = int(values[1])
    return saved_key_logs


# sum's up the two dictionary's
def sum_key_logs(saved_key_logs):
    for key in saved_key_logs:
        if key in new_key_logs:
            new_key_logs[key] += saved_key_logs[key]
        else:
            new_key_logs[key] = saved_key_logs[key]


# writes the added dictionary to the file
def write_key_logs(key_logs):
    # write file
    with open(file_path, "w") as key_log_file:
        for key in key_logs:
            key_log_file.write("{0}:{1}\n".format(key, key_logs[key]))


# saves the key logs to a text file
def key_logger():
    # reads the saved key logs and adds them to the new one
    sum_key_logs(read_saved_logs())
    while True:
        write_key_logs(new_key_logs)
        time.sleep(3)


# setup of the global key listener
def setup_key_listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


# starting the threads
if __name__ == "__main__":
    print("Key Logger started")
    t1 = threading.Thread(target=key_logger)
    t2 = threading.Thread(target=setup_key_listener)
    t1.start()
    t2.start()

