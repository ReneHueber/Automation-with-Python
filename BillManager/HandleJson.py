import json
import os


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
