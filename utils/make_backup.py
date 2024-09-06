import os
import json


def make_backup(employeeId, palletId, photo_name_list, file_path):
    json_data = {
        "employeeId": employeeId,
        "palletId": palletId,
        "photos": photo_name_list
    }
    data = []
    data.append(json_data)
    file_name = f"{file_path}/{palletId}.json"
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
