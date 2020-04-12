from BillManager.Logs import write_log
from datetime import datetime


class Bill:
    file_name = ""
    company_name = ""
    sequential_number = ""
    month = None
    year = None
    payment_status_folder = ""
    parent_folder = ""
    move_path = ""
    outgoing = True
    bill_number = 1
    file_type = ""

    bill_prefix = ""
    own_bill_unique = ""
    outgoing_bills_folder = ""
    incoming_bills_folder = ""

    def __init__(self, bill_prefix, own_bill_unique,
                 outgoing_bills_folder, incoming_bills_folder):
        self.bill_prefix = bill_prefix
        self.own_bill_unique = own_bill_unique
        self.outgoing_bills_folder = outgoing_bills_folder
        self.incoming_bills_folder = incoming_bills_folder

    # get's the information of the filename, checks if format is correct
    def set_bill_values(self, file_name):
        values = file_name.split("-")
        # bill is for a customer (outgoing)
        if is_outgoing_bill(values):
            self.month = values[0]
            self.company_name = values[1]
            self.year, self.sequential_number = get_values_sequential_number()
            self.payment_status_folder = check_bill_unpaid(values)
            self.parent_folder = self.outgoing_bills_folder
            self.outgoing = True
        # bill is for the customer (incoming)
        else:
            self.month = values[0]
            self.year = format_incoming_bill_year(values[1])
            self.company_name = values[2]
            self.payment_status_folder = check_bill_unpaid(values)
            self.parent_folder = self.incoming_bills_folder
            self.outgoing = False

        return self


# checks it it is outgoing or an incoming bill
# return True if bill is outgoing
def is_outgoing_bill(values):
    # at the outgoing bill the second value is a name
    try:
        int(values[1])
        return False
    except ValueError:
        return True


# read's the current sequential number for the file
def read_sequential_number():
    with open("/home/ich/Documents/Projekte_Andere/Rechnungen/laufende_Nummer.txt", "r") as file:
        sequel_number = file.readline()

    return sequel_number


# writes the updated sequential number to the file
# increases the sequential number by one
def write_sequential_number(sequential_number):
    year, number = sequential_number.split("-")
    sequential_number = "{:d}-{:03d}".format(int(year), int(number) + 1)
    with open("/home/ich/Documents/Projekte_Andere/Rechnungen/laufende_Nummer.txt", "w") as file:
        file.write(sequential_number)


# get's the values from the sequential number in the file, checks an modifies them, return year and number
def get_values_sequential_number():
    current_date = datetime.now()

    try:
        file_value = read_sequential_number()
        year, number = file_value.split("-")

        if current_date.year != int(year):
            year = current_date.year
            number = 0
        else:
            number = int(number)

        sequential_number = "{:d}-{:03d}".format(int(year), number)
    except ValueError:
        year = None
        sequential_number = None

    return year, sequential_number


# get's the file_name without prefix and file_type
# return the number the bill has
def get_bill_number(file_name):
    values = file_name.split("_")
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


# checks if the file name is in the right format
def check_file_name_format(file_name):
    format_okay = False
    values = file_name.split("-")
    symbols = ["_", ",", ";", "-"]

    try:
        if len(values) == 4:
            if check_number(values[0], 1, 12) and check_number(values[1], 0, 99) \
                    and check_string(values[2], symbols) and values[3] == "o":
                format_okay = True
        elif len(values) == 3:
            if check_number(values[0], 1, 12):
                if check_number(values[1], 0, 99):
                    if check_string(values[2], symbols):
                        format_okay = True
                else:
                    if check_string(values[1], symbols) and values[2] == "o":
                        format_okay = True
        elif len(values) == 2:
            if check_number(values[0], 1, 12) and check_string(values[1], symbols):
                format_okay = True
    except IndexError and ValueError:
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
def check_string(value, symbols):
    for symbol in symbols:
        if symbol in value:
            return False

    return True
