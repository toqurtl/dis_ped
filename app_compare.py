from dis_ped.app.filefinder import FileFinder
import sys
import json

idx = sys.argv[1]

finder = FileFinder("setting.json")

force_idx_list = finder.get_force_folder_list(idx)

compare_data = {}
compare_data["simul_time"] = {}
compare_data["ade"] = {}
compare_data["social"] = {}
for force_idx in force_idx_list:
    with open(finder.valid_path(idx, force_idx), 'r') as f:
        data = json.load(f)
    compare_data["simul_time"][force_idx] = data["result"]["simulation_time"]
    compare_data["ade"][force_idx] = data["result"]["ade"]
    compare_data["social"][force_idx] = data["result"]["social"]

with open(finder.compare_path(idx), 'w') as f:
    json.dump(compare_data, f, indent=4)