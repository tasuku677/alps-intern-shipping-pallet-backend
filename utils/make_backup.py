import os
import json

def make_backup(employeeId, palletId, photo_name_list, file_path):
    json_data = {
        "employeeId": employeeId,
        "palletId": palletId,
        "photos": photo_name_list
    }
    if (os.path.exists(file_path)):
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(json_data)
    with open('./info.json', "w") as json_file:
        json.dump(data, json_file, indent=4)
