import os
from shutil import copy2
from BillManager.Logs import write_log


class MoveBill:
    destination_base_folder = ""

    def __init__(self, destination_base_folder):
        self.destination_base_folder = destination_base_folder

    # moves the file to the right destination
    def move_file(self, src_path, current_bill, new_line):
        os.rename(src_path, current_bill.move_path)
        write_log("Moved \"{0}\" to \"{1}\".{2}".format(current_bill.file_name,
                                                        current_bill.move_path.split(
                                                            self.destination_base_folder + "/")[1],
                                                        new_line))

    # creates the path to move the file in the right folder
    def create_move_path(self, current_bill):
        # set's the parent folder for the bill
        current_bill.move_path = os.path.join(self.destination_base_folder, current_bill.parent_folder)
        # formats the date for the folder
        formatted_date = "{0}-{1}".format(current_bill.year, current_bill.month)
        # a list, because 3 folder layer have to be created
        move_list = [formatted_date, current_bill.company_name, current_bill.payment_status_folder]

        # creates and add's the three folder layers
        for folder in move_list:
            current_bill.move_path = os.path.join(current_bill.move_path, folder)
            create_needed_folder(current_bill.move_path)


# moves the file to the right destination
def copy_file(current_bill, copy_path):
    copy2(current_bill.move_path, copy_path)
    write_log("Copied \"{0}\" to \"{1}\".\n".format(current_bill.file_name, copy_path))


# creates the folder it's not existing
def create_needed_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
