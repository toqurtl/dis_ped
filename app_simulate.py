import numpy as np
from dis_ped.simulator import Simulator
import json
from dis_ped.app.func import Experiment
from dis_ped.app.filefinder import FileFinder
from dis_ped.utils.new_plot import SceneVisualizer
import sys

np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})

idx = sys.argv[1]
if len(sys.argv) > 2:
    force_idx = int(sys.argv[2])
else:
    force_idx = 0

with open("setting.json", 'r') as f:
    setting_data = json.load(f)

file_finder = FileFinder("setting.json")

exp = Experiment("setting.json")
exp.set_experiment(idx, force_idx)
exp.save_vid_data()

s = Simulator(
    exp.peds,
    obstacles=exp.obstacle,
    time_table=exp.video.time_table,
    force_idx=force_idx
)


s.simulate()
print(s.time_step)

s.result_to_json(exp.simul_result_path)

with SceneVisualizer(s.peds, s, exp.animation_path) as sv:
    sv.animate()        

with SceneVisualizer(s.peds, s, exp.plot_path) as sv:
    sv.plot()




    

