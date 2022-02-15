from dis_ped.config.filefinder import FileFinder
from dis_ped.config.config import PedConfig
import sys
import json

file_path = sys.argv[1]
config = PedConfig(file_path)
finder = FileFinder(file_path)

idx_list = finder.get_idx_folder_list()
compare_data = {}
# experiment
compare_data["state"] = {} 
compare_data["state"]["setting_id"] = config.setting_id
compare_data["state"]["repulsive_force"] = config.repulsive_force

# vid_info
compare_data["vid_info"] = {}
compare_data["vid_info"]["gt_time"]={}
compare_data["vid_info"]["num_person"]={}
compare_data["vid_info"]["social"]={}

for idx in idx_list:
    with open(finder.valid_path(idx), 'r') as f:
        data = json.load(f)
    compare_data["vid_info"]["gt_time"][idx] = data["basic"]["gt_time"]
    compare_data["vid_info"]["num_person"][idx] = data["basic"]["num_person"]
    compare_data["vid_info"]["social"][idx] = data["basic"]["social"]

# result
compare_data["simul_result"] = {}
compare_data["simul_result"]["success"] = {}
compare_data["simul_result"]["simul_time"] = {}
compare_data["simul_result"]["ade"] = {}
compare_data["simul_result"]["dtw"] = {}
compare_data["simul_result"]["social"] = {}

for idx in idx_list:
    with open(finder.valid_path(idx), 'r') as f:
        data = json.load(f)

    compare_data["simul_result"]["success"][idx] = data["result"]["success"]    
    compare_data["simul_result"]["simul_time"][idx] = data["result"]["simulation_time"]
    compare_data["simul_result"]["ade"][idx] = data["result"]["ade"]
    compare_data["simul_result"]["dtw"][idx] = data["result"]["dtw"]
    compare_data["simul_result"]["social"][idx] = data["result"]["social"]

# type2
compare_data_idx = {}
compare_data_idx["state"] = {} 
compare_data_idx["state"]["setting_id"] = config.setting_id
compare_data_idx["state"]["repulsive_force"] = config.repulsive_force

compare_data_idx["result"] = {}

for idx in idx_list:
    compare_data_idx["result"][idx] = {}
    compare_data_idx["result"][idx]["vid_info"] = {}
    compare_data_idx["result"][idx]["simul_result"] = {}
    with open(finder.valid_path(idx), 'r') as f:
        data = json.load(f)
    compare_data_idx["result"][idx]["vid_info"]["vid_idx"] = idx
    compare_data_idx["result"][idx]["vid_info"]["gt_time"] = data["basic"]["gt_time"]
    compare_data_idx["result"][idx]["vid_info"]["num_person"] = data["basic"]["num_person"]
    compare_data_idx["result"][idx]["vid_info"]["social"] = data["basic"]["social"]
    compare_data_idx["result"][idx]["simul_result"]["success"] = data["result"]["success"]    
    compare_data_idx["result"][idx]["simul_result"]["simul_time"] = data["result"]["simulation_time"]
    compare_data_idx["result"][idx]["simul_result"]["ade"] = data["result"]["ade"]
    compare_data_idx["result"][idx]["simul_result"]["dtw"] = data["result"]["dtw"]
    compare_data_idx["result"][idx]["simul_result"]["social"] = data["result"]["social"]


with open(finder.compare_path(), 'w') as f:
    json.dump(compare_data, f, indent=4)

with open(finder.compare_path_idx(), 'w') as f:
    json.dump(compare_data_idx, f, indent=4)