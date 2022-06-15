import os
from dis_ped.config.filefinder import FileFinder
import json
import csv
import sys



    


target_force_type = sys.argv[1]
folder_path = "C:\\Users\\toqurtl\\snucem\\exp\\result\\0326"
result_file_name = "person_"+target_force_type+"_0607_dtw.json"
result_file_name_csv = "person_"+target_force_type+"_0607_dtw.csv"

result_file_path = os.path.join(folder_path, result_file_name)
result_file_path_csv = os.path.join(folder_path, result_file_name_csv)

# force_1
# model_id_list = [1,7,6,14,13,11,10,12,15,16,17,18, 19, 20, 21, 22, 23,24,25,26,27,28,29,30,31,32,33,34]
# model_id_list = [12,16,17,15,6,19,20,21,22,1,23,24,25,26,27,28,29,30,31,32,33]

# force_2
# model_id_list =[1,7,6,13,10,9,12,8,11,14,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34, 35]
model_id_list = [16,21,11,12,10,6,18,20,23,24,1,25,26,27,28,29,30,31,32,33,34,35]


# # basic-sfm-1
# model_id_list = [1]

result_dict ={}
for folder_name in os.listdir(folder_path):
    if os.path.isdir(os.path.join(folder_path, folder_name)):
        data_path = os.path.join(folder_path, folder_name, "compare.json")
        with open(data_path, 'r') as f:
            data = json.load(f)
        force_type_of_data = data["state"]["repulsive_force"]
        if force_type_of_data == target_force_type:                    
            ade_dict = data["simul_result"]["dtw"]
            for vid_idx, ade in ade_dict.items():
                if vid_idx not in result_dict.keys():
                    result_dict[vid_idx] = {}    
                result_dict[vid_idx][folder_name] = ade

csv_f = open(result_file_path_csv, "w", newline='')
result_list=[]
model_id_list.insert(0, "idx")
result_list.append(model_id_list.copy())
model_id_list.pop(0)
for vid_name, vid_dict in result_dict.items():
    value_list=[vid_name]        
    for i in model_id_list:
        model_name = "social_sfm_2_"+str(i)
        if model_name in vid_dict.keys():
            value_list.append(vid_dict[model_name])
        else:
            value_list.append("-")
    result_list.append(value_list)
    
wr = csv.writer(csv_f)
wr.writerows(result_list)
csv_f.close()


with open(result_file_path, "w") as f:
    json.dump(result_dict, f, indent=4)



                