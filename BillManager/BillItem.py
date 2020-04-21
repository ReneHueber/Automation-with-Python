import time

from BillManager.Logs import write_log
from datetime import datetime
import os


class Bill:
    file_name = ""
    company_name = ""
    sequential_number = ""
    month = "00"
    year = "0000"
    payment_status_folder = ""
    parent_folder = ""
    move_path = ""
    outgoing = True
    bill_number = 1
    file_type = ""
    creation_date = ""
    sequential_numbers_list = []
    description = ""
    date_of_issue = "00010101"

    bill_prefix = ""
    own_bill_unique = ""
    outgoing_bills_folder = ""
    incoming_bills_folder = ""
    open_bills_folder = ""

    def __init__(self, bill_prefix, own_bill_unique,
                 outgoing_bills_folder, incoming_bills_folder,
                 open_bills_folder):
        self.bill_prefix = bill_prefix
        self.own_bill_unique = own_bill_unique
        self.outgoing_bills_folder = outgoing_bills_folder
        self.incoming_bills_folder = incoming_bills_folder
        self.open_bills_folder = open_bills_folder

    def set_bill_values(self, file_name, file_path):
        values = file_name.split("-")

        # outgoing bill
        if is_outgoing_bill(values):
            self.year, self.month = get_path_creation_date(file_path)
            self.sequential_number, self.sequential_numbers_list = get_sequential_number(self.year)
            self.company_name = values[0]
            self.payment_status_folder = check_bill_unpaid(values)
            self.parent_folder = self.outgoing_bills_folder
        # incoming bill
        else:
            # move bill in correct folder
            if values[0][0] == "~":
                value = file_name.split("~")
                folder_values = value[1].split("-")
                name_values = value[2].split("-")

                self.month = folder_values[0]
                self.year = folder_values[1]
                self.company_name = folder_values[2]

                self.description = name_values[0]
                self.date_of_issue = name_values[1]
                self.parent_folder = self.incoming_bills_folder
                self.payment_status_folder = "Bezahlt"
                self.outgoing = False
            # move bill in temporary folder
            else:
                self.company_name = values[0]
                self.description = values[1]
                self.date_of_issue = values[2]
                self.parent_folder = self.open_bills_folder
                self.payment_status_folder = "Offen"
                self.outgoing = False


# checks it it is outgoing or an incoming bill
# return True if bill is outgoing
def is_outgoing_bill(values):
    if "own" in values:
        return True
    else:
        return False


# read's the current sequential number for the file
def read_sequential_number():
    sequel_number = []
    with open("/home/ich/Dokumente/Projekte_Andere/Rechnungen/laufende_Nummer.txt", "r") as file:
        for line in file:
            sequel_number.append(line.strip().split("-"))

    return sequel_number


# writes the updated sequential number to the file
# increases the sequential number by one
def write_sequential_number(bill_year, sequential_numbers):
    for year in sequential_numbers:
        if year[0] == bill_year:
            number = int(year[1]) + 1
            year[1] = "{:03d}".format(number)

    sequential_numbers.sort()

    with open("/home/ich/Dokumente/Projekte_Andere/Rechnungen/laufende_Nummer.txt", "w") as file:
        for sequential_number in sequential_numbers:
            file.write("{0}-{1}\n".format(sequential_number[0], sequential_number[1]))


def get_sequential_number(bill_year):
    sequential_number = "000"
    years = read_sequential_number()
    number_existing = False
    for year in years:
        if year[0] == bill_year:
            number_existing = True
            sequential_number = year[1]

    if not number_existing:
        sequential_number = "{:03d}".format(0)
        new_number = [bill_year, sequential_number]
        years.append(new_number)

    return sequential_number, years


# get's the file_name without prefix and file_type
# return the number the bill has
def get_bill_number(file_name, split_char):
    values = file_name.split(split_char)
    try:
        return int(values[3])
    except IndexError:
        write_log("\tDer Filename: \"{0}\" entspricht nicht der formatierung.".format(file_name))
        return None


# format's the year if it is necessary
def format_incoming_bill_year(year):
    if len(year) == 2:
        return "20{0}".format(year)
    else:
        return year


# checks if the bill in unpaid
# returns True if the bill in unpaid
def check_bill_unpaid(values):
    if "o" in values:
        return "Offen"
    else:
        return "Bezahlt"


# get's the last date where the file has been last modified
def get_path_creation_date(file_path):
    file_time = time.gmtime(os.path.getmtime(file_path))
    month = "{:02d}".format(file_time.tm_mon)
    year = str(file_time.tm_year)

    return year, month


# checks if the file name is in the right format
def check_file_name_format(file_name):
    format_okay = False
    values = file_name.split("-")

    try:
        if len(values) == 2:
            if check_string(values[0]) and values[1] == "own":
                return True
        elif len(values) == 3:
            if check_string(values[0]) and values[1] == "own" and values[2] == "o":
                return True
            elif check_string(values[0]) and check_string(values[1]) \
                    and int(values[2]) and (len(values[2]) == 8):
                return True
    except IndexError and TypeError and ValueError:
        format_okay = False

    return format_okay


# checks if the number is bigger or equal and smaller or equal the given values
def check_number(str_number, min_value, max_include_value):
    try:
        if min_value <= int(str_number) <= max_include_value:
            return True
        else:
            return False
    except ValueError:
        return False


# checks if a list of symbols is not in a string
def check_string(value):
    symbols = ["_", ",", ";", "-"]

    for symbol in symbols:
        if symbol in value:
            return False

    return True
