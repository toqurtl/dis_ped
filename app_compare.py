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
compare_data["simul_result"]["sdcr_error"] = {}

for idx in idx_list:
    with open(finder.valid_path(idx), 'r') as f:
        data = json.load(f)

    compare_data["simul_result"]["success"][idx] = data["result"]["success"]    
    compare_data["simul_result"]["simul_time"][idx] = data["result"]["simulation_time"]
    compare_data["simul_result"]["ade"][idx] = data["result"]["ade"]
    compare_data["simul_result"]["dtw"][idx] = data["result"]["dtw"]
    compare_data["simul_result"]["social"][idx] = data["result"]["social"]
    compare_data["simul_result"]["sdcr_error"][idx] = data["result"]["sdcr_error"]

# type2
compare_data_idx = {}
compare_data_idx["state"] = {} 
compare_data_idx["state"]["setting_id"] = config.setting_id
compare_data_idx["state"]["repulsive_force"] = config.repulsive_force

compare_data_idx["result"] = {}

ade_avg, ade_avg_high, ade_avg_low = 0, 0, 0
dtw_avg, dtw_avg_high, dtw_avg_low = 0, 0, 0
social_avg =0
ctn, ctn_high, ctn_low = 0, 0, 0
for idx in idx_list:
    compare_data_idx["result"][idx] = {}
    compare_data_idx["result"][idx]["vid_info"] = {}
    compare_data_idx["result"][idx]["simul_result"] = {}
    with open(finder.valid_path(idx), 'r') as f:
        data = json.load(f)

    ade = data["result"]["ade"]
    dtw = data["result"]["dtw"]
    social = data["result"]["social"]
    success = data["result"]["success"]
    vid_social = data["basic"]["social"]
    compare_data_idx["result"][idx]["vid_info"]["vid_idx"] = idx
    compare_data_idx["result"][idx]["vid_info"]["gt_time"] = data["basic"]["gt_time"]
    compare_data_idx["result"][idx]["vid_info"]["num_person"] = data["basic"]["num_person"]
    compare_data_idx["result"][idx]["vid_info"]["social"] = vid_social
    compare_data_idx["result"][idx]["simul_result"]["success"] = success
    compare_data_idx["result"][idx]["simul_result"]["simul_time"] = data["result"]["simulation_time"]
    compare_data_idx["result"][idx]["simul_result"]["ade"] = ade
    compare_data_idx["result"][idx]["simul_result"]["dtw"] = dtw
    compare_data_idx["result"][idx]["simul_result"]["social"] = social
    compare_data_idx["result"][idx]["simul_result"]["sdcr_error"] = data["result"]["sdcr_error"]
    if success:
        ade_avg += ade
        dtw_avg += dtw
        social_avg += social
        ctn += 1
        if vid_social > 0.22:
            ade_avg_low += ade
            dtw_avg_low += dtw
            ctn_low += 1
        else:
            ade_avg_high += ade
            dtw_avg_high += dtw
            ctn_high += 1

ade_avg = ade_avg/ctn
dtw_avg = dtw_avg/ctn
social_avg = social_avg/ctn
ade_avg_low, dtw_avg_low = ade_avg_low/ctn_low, dtw_avg_low/ctn_low
ade_avg_high, dtw_avg_high = ade_avg_high/ctn_high, dtw_avg_high/ctn_high

compare_data_idx["state"]["ade_avg"] = ade_avg
compare_data_idx["state"]["dtw_avg"] = dtw_avg
compare_data_idx["state"]["social_avg"] = social_avg
compare_data_idx["state"]["ctn"] = ctn
compare_data_idx["state"]["ade_avg_low"] = ade_avg_low
compare_data_idx["state"]["dtw_avg_low"] = dtw_avg_low
compare_data_idx["state"]["ctn_low"] = ctn_low
compare_data_idx["state"]["ade_avg_high"] = ade_avg_high
compare_data_idx["state"]["dtw_avg_high"] = dtw_avg_high
compare_data_idx["state"]["ctn_high"] = ctn_high

compare_data["state"]["ade_avg"] = ade_avg
compare_data["state"]["dtw_avg"] = dtw_avg
compare_data["state"]["social_avg"] = social_avg
compare_data["state"]["ctn"] = ctn


with open(finder.compare_path(), 'w') as f:
    json.dump(compare_data, f, indent=4)

with open(finder.compare_path_idx(), 'w') as f:
    json.dump(compare_data_idx, f, indent=4)