from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog to make it work

from datetime import datetime
import os
import time


# wait's until the file is "complete" if it is downloaded
def check_file_complete(path):
    file_complete = False
    try:
        while not file_complete:
            file_size = os.path.getsize(path)
            time.sleep(0.5)
            if file_size != os.path.getsize(path):
                file_complete = False
            else:
                time.sleep(0.5)
                file_complete = True
    except FileNotFoundError:
        time.sleep(1)

    return file_complete


# get's the correct filename and the type
def get_file_name_type(file_path):
    file_name = os.path.split(file_path)[-1]
    try:
        file_type = file_name.split(".")[-1]
    except ValueError:
        file_type = ""

    return file_name, file_type


# creates the a folder with the wished name if it dos'nt exists
def create_folder_if_not_existing(base_path, check_name):
    wished_path = os.path.join(base_path, check_name)
    # path is not existing
    if not os.path.exists(wished_path):
        os.mkdir(wished_path)

    return wished_path


# get's the current date and formats it to create a new folder
def get_date_and_format():
    date = datetime.now()
    return "{:02d}_{:02d}_{:04d}".format(date.day, date.month, date.year)


# adds a number at the end of the filename
def rename_if_existing(filename, file_type, increment):
    filename_without_ending = filename.split("." + file_type)[0]
    return "{0}_{1}.{2}".format(filename_without_ending, increment, file_type)


# check if the filename exist in the destination folder
def filename_existing(destination_path, check_name):
    for existing_filename in os.listdir(destination_path):
        if existing_filename == check_name:
            return True

    return False


# custom handler for the changes in the file system
class MyHandler(FileSystemEventHandler):
    moved_file = ""

    # if a file is modified
    def on_modified(self, event):
        # check if the file exists if it has been moved before and if ist not the folder we look at
        if not os.path.isdir(event.src_path) and os.path.exists(event.src_path) \
                and not event.src_path == self.moved_file:
            rename = check_file_complete(event.src_path)
            # if the file is complete
            if rename:
                # self.last_file = event.src_path
                filename, file_type = get_file_name_type(event.src_path)
                # creates the folder for the file type
                new_destination = create_folder_if_not_existing(folder_to_track, file_type)
                # get's the current date
                current_date = get_date_and_format()
                # creates the folder for the date
                new_destination = create_folder_if_not_existing(new_destination, current_date)

                # renames the file als long as the name exist in the folder
                file_incrementer = 1
                # to add the increment right
                new_filename = filename
                while filename_existing(new_destination, new_filename):
                    new_filename = rename_if_existing(filename, file_type, file_incrementer)
                    file_incrementer += 1

                # renames the file
                destination_path = os.path.join(new_destination, new_filename)
                self.moved_file = destination_path
                os.rename(event.src_path, destination_path)
                print(f"Moved: {new_filename}")


folder_to_track = "/home/ich/Downloads"
event_handler = MyHandler()

# starting the observer and keep it running until you enter "control + c"
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
