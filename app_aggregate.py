from dis_ped.app.filefinder import FileFinder
import os
import json
import csv


finder = FileFinder("setting_2.json")
first_row = []

first_row += ["vid_idx", "success", "num_person", "time_1", "time_2", "time_3"]
first_row += ["ade_1", "ade_2", "ade_3", "social_1", "social_2","social_3"]

f = open(finder.result_csv_path, "w", newline='')
wr = csv.writer(f)
wr.writerow(first_row)

for compare_path in finder.get_compare_json_path_list():
    idx = compare_path.split("\\")[-2]
    
    with open(finder.basic_path(idx), "r", encoding="UTF-8") as f:
        num_person = json.load(f)["basic"]["num_person"]

    with open(compare_path, "r", encoding="UTF-8") as f:
        data = json.load(f)

    success = data["state"]["success"]
    row = [idx, success, num_person]
    if success:
        for s in data["simul_time"].values():
            row.append(s)
        
        for s in data["ade"].values():
            row.append(s)

        for s in data["social"].values():
            row.append(s)
    else:
        for i in range(0, 9):
            row.append(0)
    wr.writerow(row)
f.close()

    
    