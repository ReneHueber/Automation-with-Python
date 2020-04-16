import os
from BillManager.Logs import write_log
from BillManager import BillItem


# check's if the file name already exists
# if it exists it, return true
def check_file_name_existing(current_bill):
    for existing_file_name in os.listdir(current_bill.move_path):
        if existing_file_name == current_bill.file_name:
            return True

    return False


def get_next_bill_number(bill):
    number = 0
    files = []
    parent_folder = os.path.dirname(bill.move_path)
    for folder in os.listdir(parent_folder):
        for file_name in os.listdir(os.path.join(parent_folder, folder)):
            files.append(file_name)

    if len(files) > 0:
        for file in files:
            file_name_short = file.split(bill.bill_prefix)[1].split("." + bill.file_type)[0]
            current_number = BillItem.get_bill_number(file_name_short)
            if current_number > number:
                number = current_number

        return number + 1
    else:
        return 1


# renames the bills in the right format, depending on the bill type (incoming, outgoing)
def rename_file(bill):
    old_file_name = bill.file_name
    # check's if the file is open and add's the right symbol
    add_open = ""
    if bill.payment_status_folder == "Offen":
        add_open = "_o"

    # renames the incoming bill
    if not bill.outgoing:
        bill.file_name = "{prefix}{month}_{year}_{company}_{bill_number}{payment_status}.{type}".format(
            prefix=bill.bill_prefix, month=bill.month, year=bill.year, company=bill.company_name,
            bill_number=bill.bill_number, payment_status=add_open, type=bill.file_type)

        write_log("\tRenamed incoming Bill \"{0}\" to \"{1}\".".format(old_file_name, bill.file_name))
    # renames the outgoing bill
    else:
        bill.file_name = "{prefix}{month}_{year}-{sequel_number}_{company}_{unique}{payment_status}.{type}".format(
            prefix=bill.bill_prefix, month=bill.month, year=bill.year, sequel_number=bill.sequential_number,
            company=bill.company_name, unique=bill.own_bill_unique, payment_status=add_open, type=bill.file_type)

        write_log("\tRenamed outgoing Bill \"{0}\" to \"{1}\".".format(old_file_name, bill.file_name))
