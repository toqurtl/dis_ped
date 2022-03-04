import numpy as np
from dis_ped.simulator import Simulator
import json
from dis_ped.config.exp_setting import ExperimentSetting
from dis_ped.config.filefinder import FileFinder
from dis_ped.utils.new_plot import SceneVisualizer
import sys

np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})

idx = sys.argv[1]
config_path = sys.argv[2]
if len(sys.argv) == 5:
    is_animated = sys.argv[3]
    if is_animated == "true":
        is_animated = True
    else:
        is_animated = False
else:
    is_animated = False

file_finder = FileFinder(config_path)
exp = ExperimentSetting(config_path, idx)
# try:

s = Simulator(exp)

s.simulate()
s.result_to_json(file_finder.simul_result_path(idx))
if s.time_step > file_finder.simul_time_threshold:
    file_finder.summary_to_json(idx, False)
    print("simul_time_threshold!")
else:
    file_finder.summary_to_json(idx, True)
    if is_animated:
        with SceneVisualizer(s.peds, s, exp.animation_path) as sv:
            sv.animate()        
        with SceneVisualizer(s.peds, s, exp.plot_path) as sv:
            sv.plot()

# except Exception as e:
#     file_finder.summary_to_json(idx, False)
#     print("error during simulation")
#     print(e)
    




    

