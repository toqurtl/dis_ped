from dis_ped.config.filefinder import FileFinder
import sys
import json
import csv

file_path = sys.argv[1]

finder = FileFinder(file_path)
first_row = []

first_row += ["vid_idx", "video_time", "num_person", "social"]
first_row += ["success", "simul_time_error", "ade", "dtw", "social"]

f = open(finder.result_csv_path, "w", newline='')
wr = csv.writer(f)
wr.writerow(first_row)

compare_path= finder.compare_path_idx()

with open(compare_path, "r", encoding="UTF-8") as f:
    data = json.load(f)


for vid_idx, result in data["result"].items():
    row = []
    for data in result["vid_info"].values():
        row.append(data)

    for data in result["simul_result"].values():
        row.append(data)
  
    wr.writerow(row)
    
f.close()


