import os
from dis_ped.config.filefinder import FileFinder
import json
import csv

folder_path = "C:\\Users\\toqurtl\\snucem\\exp\\result\\0326"
file_name = "compare_idx.json"
result_file_name = "compare_model.csv"
first_row = ["model_id", "type"]
first_row += ["ade_avg", "dtw_avg", "social_avg", "ctn"]
first_row += ["ade_avg_low", "dtw_avg_low", "ctn_low"]
first_row += ["ade_avg_high", "dtw_avg_high", "ctn_high"]
first_row += ["ade_avg_many", "dtw_avg_many", "ctn_many"]
first_row += ["ade_avg_few", "dtw_avg_few", "ctn_few"]
first_row += ["ade_avg_sdcr", "dtw_avg_sdcr", "ctn_sdcr"]

result_file_path = os.path.join(folder_path, result_file_name)
csv_f = open(result_file_path, "w", newline='')
wr = csv.writer(csv_f)
wr.writerow(first_row)


for folder_name in os.listdir(folder_path):
    if folder_name.split(".")[-1] != "csv":
        model_path = os.path.join(folder_path, folder_name)
        print(model_path)
        if file_name in os.listdir(model_path):
            file_path = os.path.join(model_path, file_name)
            with open(file_path, 'r') as f:
                data = json.load(f)
            row = []            
            for x in data["state"].values():                
                if type(x) is dict:                                        
                    for y in x.values():                        
                        row.append(y)
                else:
                    row.append(x)
            wr.writerow(row)
csv_f.close()