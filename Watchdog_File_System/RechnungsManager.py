from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog to make it work

from datetime import datetime
import os
import time
import json

# if folders or prefix are changed, change them here
track_folder = "/home/ich/Desktop/Move_Folder"
destination_base_folder = "/home/ich/Documents/Projekte_Andere/Rechnungen"
json_file_path = "/home/ich/Documents/Projekte_Andere/Rechnungen/open_bills.txt"
# TODO maybe remove bill_prefix and add it in the program
bill_prefix = "Rechnung-"
own_bill_unique = "Sonnenseite"
outgoing_bills_folder = "Rechnungen_von_Mir"
incoming_bills_folder = "Rechnungen_an_Mich"


# object for the bills to handle data management better
class Bill:
    file_name = ""
    company_name = ""
    month = None
    year = None
    unpaid = ""
    parent_folder = ""
    move_path = ""
    outgoing = True


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

    file_name_without_ending = file_name.split("." + file_type)[0]

    return file_name, file_type, file_name_without_ending


# get's the information of the filename
def get_bill_values(file_name):
    current_bill = Bill()
    values_string = file_name.split(bill_prefix)[1]
    values = values_string.split("_")
    # bill is for a customer (outgoing)
    if own_bill_unique in values:
        current_bill.month = values[0]
        current_bill.year = values[1].split("-")[0]
        current_bill.company_name = values[2]
        current_bill.unpaid = check_bill_unpaid(5, values)
        current_bill.parent_folder = outgoing_bills_folder
        current_bill.outgoing = True
    # bill is for the customer (incoming)
    else:
        current_bill.month = values[0]
        current_bill.year = format_incoming_bill_year(values[1])
        current_bill.company_name = values[2]
        current_bill.unpaid = check_bill_unpaid(4, values)
        current_bill.parent_folder = incoming_bills_folder
        current_bill.outgoing = False

    return current_bill


# format's the year if it is necessary
def format_incoming_bill_year(year):
    if len(year) == 2:
        return "20{0}".format(year)
    else:
        return year


# checks if the bill in unpaid
# returns True if the bill in unpaid
def check_bill_unpaid(unpaid_length, values):
    if len(values) == unpaid_length:
        return "Offen"
    else:
        return "Bezahlt"


# creates the folder it's not existing
def create_needed_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


# creates the path to move the file in the right folder
def create_move_path(current_bill):
    # set's the parent folder for the bill
    current_bill.move_path = os.path.join(destination_base_folder, current_bill.parent_folder)
    # formats the date for the folder
    formatted_date = "{0}-{1}".format(current_bill.year, current_bill.month)
    # a list, because 3 folder layer have to be created
    move_list = [formatted_date, current_bill.company_name, current_bill.unpaid]

    # creates and add's the three folder layers
    for folder in move_list:
        current_bill.move_path = os.path.join(current_bill.move_path, folder)
        create_needed_folder(current_bill.move_path)

    # add's the filename to the new path
    current_bill.move_path = os.path.join(current_bill.move_path, current_bill.file_name)
    check_add_open_bill(current_bill)


# checks if the bill is unpaid and adds it to the dictionary to be written in the json file
def check_add_open_bill(current_bill):
    if current_bill.unpaid == "Offen":
        if current_bill.outgoing:
            open_bills["bills_outgoing"].append({
                "company_name": current_bill.company_name,
                "file_name": current_bill.file_name,
                "file_path": current_bill.move_path
            })
        else:
            open_bills["bills_incoming"].append({
                "company_name": current_bill.company_name,
                "file_name": current_bill.file_name,
                "file_path": current_bill.move_path
            })

    write_json_to_file()


# moves the file to the right destination
def move_file(src_path, current_bill):
    os.rename(src_path, current_bill.move_path)


# call's all the functions necessary to create the folders and moves the file
def handle_bill_move(event):
    # only rename if it is not a directory
    if not os.path.isdir(event.src_path) and os.path.exists(event.src_path):
        # checks if the file is moved completely
        start_move = check_file_complete(event.src_path)
        # if it is moved completely it can be moved
        if start_move:
            # get's the file name, type an the name without the file type
            file_name, file_type, file_name_without_ending = get_file_name_type(event.src_path)
            # get's the values of the file name
            bill = get_bill_values(file_name_without_ending)
            bill.file_name = file_name
            create_move_path(bill)
            move_file(event.src_path, bill)


# writes the data to the json file
def write_json_to_file():
    with open(json_file_path, "w") as outfile:
        json.dump(open_bills, outfile)


# read's the data for the json file
def read_json_from_file():
    data = {}
    if os.path.getsize(json_file_path) != 0:
        with open(json_file_path) as json_file:
            data = json.load(json_file)
    else:
        data["bills_incoming"] = []
        data["bills_outgoing"] = []

    return data


class MyHandler(FileSystemEventHandler):
    moved_file = ""

    # file has been created
    def on_created(self, event):
        handle_bill_move(event)

    # if a file is modified
    def on_modified(self, event):
        handle_bill_move(event)


# reads the json file if it's not empty, otherwise creates it
open_bills = read_json_from_file()
event_handler = MyHandler()

# starting the observer and keep it running until you enter "control + c"
observer = Observer()
observer.schedule(event_handler, track_folder, recursive=True)
observer.start()
print("Watcher started")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
