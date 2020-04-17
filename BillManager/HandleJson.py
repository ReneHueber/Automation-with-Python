import json
import os
from BillManager.Logs import write_log


class HandleJson:
    json_file_path = ""

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    # writes the data to the json file
    def write_json_to_file(self, open_bills):
        with open(self.json_file_path, "w") as outfile:
            json.dump(open_bills, outfile)

    # read's the data for the json file
    def read_json_from_file(self):
        data = {}
        if os.path.getsize(self.json_file_path) != 0:
            with open(self.json_file_path) as json_file:
                data = json.load(json_file)
        else:
            data["bills_incoming"] = []
            data["bills_outgoing"] = []

        return data


# add's an unpaid bill to the dict
def add_dict_json(bill, open_bills, dict_key, bill_type):
    open_bills[dict_key].append({
        "company_name": bill.company_name,
        "month": bill.month,
        "year": bill.year,
        "file_name": bill.file_name,
        "file_path": bill.move_path,
        "description": bill.description,
        "date_of_issue": bill.date_of_issue
    })
    write_log(
        "\tAdd {0} open Bill \"{1}\" from {2}.".format(bill_type, bill.file_name, bill.company_name))
