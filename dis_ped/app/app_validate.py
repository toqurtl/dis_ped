import sys
from dis_ped.video.result_data import ResultData
from dis_ped.config.filefinder import FileFinder
import json


idx = sys.argv[1]
file_path = sys.argv[2]

    
file_finder = FileFinder(file_path)
trajectory_path = file_finder.simul_result_path(idx)
gt_path = file_finder.gt_path(idx)
valid_path = file_finder.valid_path(idx)
vid_info_path = file_finder.video_info_path(idx)
summary_path = file_finder.summary_path(idx)

with open(summary_path, "r") as f:
    summary = bool(json.load(f)["success"])


result_data = ResultData(trajectory_path, gt_path)
with open(vid_info_path, "r") as f:
    data = json.load(f)

data["basic"]["social"] = result_data.risk_index_of_video_scene(2)
with open(vid_info_path, "w") as f:
    json.dump(data, f, indent=4)

result_data.to_json(valid_path, idx, file_finder.cfg.force_name, summary)