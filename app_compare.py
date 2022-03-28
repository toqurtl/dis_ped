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

compare_data_idx["state"]["total"]= {
    "ade":0,
    "dtw":0,
    "social":0,
    "ctn":0
}
compare_data_idx["state"]["low"]= {
    "ade":0,
    "dtw":0,
    "ctn":0
}
compare_data_idx["state"]["high"]= {
    "ade":0,
    "dtw":0,
    "ctn":0
}
compare_data_idx["state"]["many_person"]= {
    "ade":0,
    "dtw":0,
    "ctn":0
}
compare_data_idx["state"]["few_person"]= {
    "ade":0,
    "dtw":0,
    "ctn":0
}
compare_data_idx["state"]["sdcr"] = {
    "ade":0,
    "dtw":0,
    "ctn":0
}


compare_data_idx["result"] = {}

ade_avg, ade_avg_high, ade_avg_low = 0, 0, 0
dtw_avg, dtw_avg_high, dtw_avg_low = 0, 0, 0
ade_low_error, dtw_low_error = 0, 0
ade_high_error, dtw_high_error = 0, 0
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
    sdcr_error = data["result"]["sdcr_error"]
    num_person = data["basic"]["num_person"]
    compare_data_idx["result"][idx]["vid_info"]["vid_idx"] = idx
    compare_data_idx["result"][idx]["vid_info"]["gt_time"] = data["basic"]["gt_time"]
    compare_data_idx["result"][idx]["vid_info"]["num_person"] = num_person
    compare_data_idx["result"][idx]["vid_info"]["social"] = vid_social
    compare_data_idx["result"][idx]["simul_result"]["success"] = success
    compare_data_idx["result"][idx]["simul_result"]["simul_time"] = data["result"]["simulation_time"]
    compare_data_idx["result"][idx]["simul_result"]["ade"] = ade
    compare_data_idx["result"][idx]["simul_result"]["dtw"] = dtw
    compare_data_idx["result"][idx]["simul_result"]["social"] = social
    compare_data_idx["result"][idx]["simul_result"]["sdcr_error"] = sdcr_error
    if success:        
        compare_data_idx["state"]["total"]["ade"] += ade
        compare_data_idx["state"]["total"]["dtw"] += dtw
        compare_data_idx["state"]["total"]["social"] += social
        compare_data_idx["state"]["total"]["ctn"] += 1
        if vid_social > 0.22:
            compare_data_idx["state"]["low"]["ade"] += ade
            compare_data_idx["state"]["low"]["dtw"] += dtw
            compare_data_idx["state"]["low"]["ctn"] += 1
        else:
            compare_data_idx["state"]["high"]["ade"] += ade
            compare_data_idx["state"]["high"]["dtw"] += dtw
            compare_data_idx["state"]["high"]["ctn"] += 1
        
        if abs(sdcr_error) < 0.1:
            compare_data_idx["state"]["sdcr"]["ade"] += ade
            compare_data_idx["state"]["sdcr"]["dtw"] += dtw
            compare_data_idx["state"]["sdcr"]["ctn"] += 1
        
        if num_person > 4:
            compare_data_idx["state"]["many_person"]["ade"] += ade
            compare_data_idx["state"]["many_person"]["dtw"] += dtw
            compare_data_idx["state"]["many_person"]["ctn"] += 1
        else:
            compare_data_idx["state"]["few_person"]["ade"] += ade
            compare_data_idx["state"]["few_person"]["dtw"] += dtw
            compare_data_idx["state"]["few_person"]["ctn"] += 1


compare_data_idx["state"]["total"]["ade"] /= compare_data_idx["state"]["total"]["ctn"]
compare_data_idx["state"]["total"]["dtw"] /= compare_data_idx["state"]["total"]["ctn"]
compare_data_idx["state"]["total"]["social"] /= compare_data_idx["state"]["total"]["ctn"]
compare_data_idx["state"]["low"]["ade"] /= compare_data_idx["state"]["low"]["ctn"]
compare_data_idx["state"]["low"]["dtw"] /= compare_data_idx["state"]["low"]["ctn"]
compare_data_idx["state"]["high"]["ade"] /= compare_data_idx["state"]["high"]["ctn"]
compare_data_idx["state"]["high"]["dtw"] /= compare_data_idx["state"]["high"]["ctn"]
compare_data_idx["state"]["sdcr"]["ade"] /= compare_data_idx["state"]["sdcr"]["ctn"]
compare_data_idx["state"]["sdcr"]["dtw"] /= compare_data_idx["state"]["sdcr"]["ctn"]
compare_data_idx["state"]["many_person"]["ade"] /= compare_data_idx["state"]["many_person"]["ctn"]
compare_data_idx["state"]["many_person"]["dtw"] /= compare_data_idx["state"]["many_person"]["ctn"]
compare_data_idx["state"]["few_person"]["ade"] /= compare_data_idx["state"]["few_person"]["ctn"]
compare_data_idx["state"]["few_person"]["dtw"] /= compare_data_idx["state"]["few_person"]["ctn"]

with open(finder.compare_path(), 'w') as f:
    json.dump(compare_data, f, indent=4)

with open(finder.compare_path_idx(), 'w') as f:
    json.dump(compare_data_idx, f, indent=4)