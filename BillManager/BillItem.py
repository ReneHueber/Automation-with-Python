from BillManager.Logs import write_log


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
        try:
            values_string = file_name.split(self.bill_prefix)[1]
            values = values_string.split("_")
            # bill is for a customer (outgoing)
            if self.own_bill_unique in values:
                self.month = values[0]
                self.year = values[1].split("-")[0]
                self.sequential_number = values[1]
                self.company_name = values[2]
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
        except IndexError:
            write_log("\tDer Filename: \"{0}\" entspricht nicht der formatierung.".format(file_name))
            return None


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
