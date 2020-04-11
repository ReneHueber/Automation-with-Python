import os
from BillManager.Logs import write_log


# check's if the file name already exists
# if it exists it, return true
def check_file_name_existing(current_bill):
    for existing_file_name in os.listdir(current_bill.move_path):
        if existing_file_name == current_bill.file_name:
            return True

    return False


# renames the file if the filename exists, add's a number after the company name, if the bill is an incoming bill
def rename_file_if_existing(bill, bill_prefix):
    old_file_name = bill.file_name
    # check's if the file is open and add's the right symbol
    add_open = ""
    if bill.payment_status_folder == "Offen":
        add_open = "_o"

    # add's a number after the company
    bill.file_name = "{prefix}{month}_{year}_{company}_{increment}{payment_status}.{type}" \
                     "".format(prefix=bill_prefix, month=bill.month, year=bill.year,
                               company=bill.company_name, increment=bill.increment,
                               payment_status=add_open, type=bill.file_type)

    write_log("\tRenamed incoming Bill \"{0}\" to \"{1}\".".format(old_file_name, bill.file_name))
    bill.increment += 1


# changes the file name as long as there is file that has the same name
# add's a number after the company that get's increased
def handle_same_name(current_bill, bill_prefix):
    file_name_existing = False
    # only renames if the bill is incoming, because the outgoing bills have a sequential number
    if not current_bill.outgoing:
        while check_file_name_existing(current_bill):
            rename_file_if_existing(current_bill, bill_prefix)
    else:
        file_name_existing = check_file_name_existing(current_bill)

    # add's the filename to the new path
    current_bill.move_path = os.path.join(current_bill.move_path, current_bill.file_name)
    # to check if the file name exists by an outgoing bill
    return file_name_existing
