from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog to make it work

import os
import time
from BillManager.Logs import write_log
from BillManager import HandleJson
from BillManager import BillItem
from BillManager import MoveBill
from BillManager import RenameBill

# if folders or prefix are changed, change them here
track_folder = "/home/ich/Desktop/Move_Folder"
destination_base_folder = "/home/ich/Documents/Projekte_Andere/Rechnungen"
json_file_path = "/home/ich/Documents/Projekte_Andere/Rechnungen/open_bills.txt"
log_file_path = "/home/ich/Desktop/Log_file.txt"
bill_prefix = "Rechnung-"
own_bill_unique = "Sonnenseite"
outgoing_bills_folder = "Rechnungen_von_Mir"
incoming_bills_folder = "Rechnungen_an_Mich"
copy_path = "/home/ich/Desktop/Rechnungen_senden"

moved_src_path = ""

handle_json = HandleJson.HandleJson(json_file_path)
move_bill = MoveBill.MoveBill(destination_base_folder)


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


# checks if the bill is unpaid and adds it to the dictionary to be written in the json file
def check_add_open_bill(current_bill):
    if current_bill.payment_status_folder == "Offen":
        # get's the values every time before writing for the json file,
        # because the values can change while the program is running
        open_bills = handle_json.read_json_from_file()
        if current_bill.outgoing:
            HandleJson.add_dict_json(current_bill, open_bills, "bills_outgoing", "Outgoing")
        else:
            HandleJson.add_dict_json(current_bill, open_bills, "bills_incoming", "Incoming")

        handle_json.write_json_to_file(open_bills)


# call's all the functions necessary to create the folders and moves the file
def handle_bill_move(event):
    # only rename if it is not a directory
    if not os.path.isdir(event.src_path) and os.path.exists(event.src_path):
        # checks if the file is moved completely
        start_move = check_file_complete(event.src_path)
        # if it file is complete it can be moved
        if start_move:
            bill = BillItem.Bill(bill_prefix, own_bill_unique,
                                 outgoing_bills_folder, incoming_bills_folder)
            # get's the file name, type an the name without the file type
            file_name, file_type, file_name_without_ending = get_file_name_type(event.src_path)
            # format_okay = BillItem.check_file_name_format(file_name_without_ending)
            # TODO check format
            format_okay = True
            if format_okay:
                # get's the creation date of the path
                bill.file_type = file_type
                # get's the values of the file name
                bill.set_bill_values(file_name_without_ending, event.src_path)

                # file name in the right format to extract data
                bill.file_name = file_name
                move_bill.create_move_path(bill)

                # get's the bill number for the incoming billA
                if not bill.outgoing:
                    bill.bill_number = RenameBill.get_next_bill_number(bill)
                # renames the bills in the correct format
                RenameBill.rename_file(bill)
                file_name_existing = RenameBill.check_file_name_existing(bill)

                if not file_name_existing:
                    # check's if the bill in unpaid and in this case add's it to the json file
                    check_add_open_bill(bill)
                    bill.move_path = os.path.join(bill.move_path, bill.file_name)

                    # moves the file and copy's it if the file is outgoing
                    if bill.outgoing:
                        move_bill.move_file(event.src_path, bill, "")
                        MoveBill.copy_file(bill, copy_path)
                        # increases the sequential number and writes it to the file
                        BillItem.write_sequential_number(bill.year, bill.sequential_numbers_list)
                    else:
                        move_bill.move_file(event.src_path, bill, "\n")
                    return True
                else:
                    write_log("\tDie Rechnung mit dem Namen \"{0}\" existiert bereits, "
                              "daher wurde sie nicht verschoben.".format(bill.file_name))
                    return False
            else:
                write_log("\tDer Filename: \"{0}\" entspricht nicht der formatierung.".format(file_name))
                return False
        else:
            return False
    else:
        return False


class MyHandler(FileSystemEventHandler):
    file_format_correct = True

    # file has been created
    def on_created(self, event):
        if not os.path.isdir(event.src_path):
            self.file_format_correct = handle_bill_move(event)

    # if a file is modified
    def on_modified(self, event):
        if self.file_format_correct and not os.path.isdir(event.src_path):
            self.file_format_correct = handle_bill_move(event)


event_handler = MyHandler()

# starting the observer and keep it running until you enter "control + c"
observer = Observer()
observer.schedule(event_handler, track_folder, recursive=True)
observer.start()
write_log("Watcher started!")

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
