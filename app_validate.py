from dataclasses import Field
import sys
import json
import numpy as np
import os
from dis_ped.video.result_data import ResultData
from dis_ped.app.func import Experiment
from dis_ped.app.filefinder import FileFinder

idx = sys.argv[1]
force_idx = sys.argv[2]
file_path = sys.argv[3]

    
file_finder = FileFinder(file_path)
trajectory_path = file_finder.simul_result_path(idx, force_idx)
gt_path = file_finder.gt_path(idx)
valid_path = file_finder.valid_path(idx, force_idx)

result_data = ResultData(trajectory_path, gt_path)
result_data.to_json(valid_path, idx, force_idx)