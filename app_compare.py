from dis_ped.app.filefinder import FileFinder
import sys
import json

idx = sys.argv[1]

finder = FileFinder("setting_2.json")

force_idx_list = finder.get_force_folder_list(idx)

if finder.is_comparable(idx):
    compare_data = {}
    compare_data["state"] = {}    
    compare_data["state"]["success"] = True   
    compare_data["simul_time"] = {}
    compare_data["ade"] = {}
    compare_data["social"] = {}
    for force_idx in force_idx_list:
        with open(finder.valid_path(idx, force_idx), 'r') as f:
            data = json.load(f)

        with open(finder.summary_path(idx, force_idx), 'r') as f:
            success = bool(json.load(f)["success"])
        
        if not success:
            compare_data["state"]["success"] = False
            continue

        compare_data["simul_time"][force_idx] = data["result"]["simulation_time"]
        compare_data["ade"][force_idx] = data["result"]["ade"]
        compare_data["social"][force_idx] = data["result"]["social"]
        compare_data["state"]["num_person"] = data["basic"]["num_person"]
    with open(finder.compare_path(idx), 'w') as f:
        json.dump(compare_data, f, indent=4)
else:
    compare_data = {}
    compare_data["state"] = {}
    compare_data["state"]["success"] = False
    with open(finder.compare_path(idx), 'w') as f:
        json.dump(compare_data, f, indent=4)
    