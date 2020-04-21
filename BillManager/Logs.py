from datetime import datetime
log_file_path = "/home/ich/Schreibtisch/Log_file.txt"


# writes a log to the log file
def write_log(log):
    # get's the time for the log
    date_time = datetime.now()
    time_log = date_time.strftime("%d/%m/%Y, %H:%M:%S")
    log_text = "{0}:\t{1}\n".format(time_log, log)

    # add's an emtpy line if the Watcher start's new, for the format
    if log == "Watcher started!":
        log_text = "\n{0}".format(log_text)

    # writes to the file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_text)