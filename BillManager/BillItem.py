

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
    increment = 2
    file_type = ""

    # get's the information of the filename, checks if format is correct
    def get_bill_values(self, file_name, current_bill):
        try:
            values_string = file_name.split(bill_prefix)[1]
            values = values_string.split("_")
            # bill is for a customer (outgoing)
            if own_bill_unique in values:
                current_bill.month = values[0]
                current_bill.year = values[1].split("-")[0]
                current_bill.sequential_number = values[1]
                current_bill.company_name = values[2]
                current_bill.payment_status_folder = check_bill_unpaid(5, values)
                current_bill.parent_folder = outgoing_bills_folder
                current_bill.outgoing = True
            # bill is for the customer (incoming)
            else:
                current_bill.month = values[0]
                current_bill.year = format_incoming_bill_year(values[1])
                current_bill.company_name = values[2]
                current_bill.payment_status_folder = check_bill_unpaid(4, values)
                current_bill.parent_folder = incoming_bills_folder
                current_bill.outgoing = False

            return current_bill
        except IndexError:
            write_log("\tDer Filename: \"{0}\" entspricht nicht der formatierung.".format(file_name))
            return None