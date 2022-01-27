import numpy as np
from dis_ped.simulator import Simulator
import json
from dis_ped.app.func import Experiment
from dis_ped.app.filefinder import FileFinder
from dis_ped.utils.new_plot import SceneVisualizer
import sys

np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})

idx = sys.argv[1]
force_idx = int(sys.argv[2])
file_path = sys.argv[3]

file_finder = FileFinder(file_path)

try:    

    exp = Experiment(file_path)
    exp.set_experiment(idx, force_idx)
    exp.save_vid_data()

    s = Simulator(
        exp.peds,
        obstacles=exp.obstacle,
        time_table=exp.video.time_table,
        force_idx=force_idx
    )


    s.simulate()
    s.result_to_json(file_finder.simul_result_path(idx, force_idx))
    if s.time_step > file_finder.simul_time_threshold:
        file_finder.summary_to_json(idx, force_idx, False)
        print("simul_time_threshold!")
    else:
        file_finder.summary_to_json(idx, force_idx, True)

        # with SceneVisualizer(s.peds, s, exp.animation_path) as sv:
        #     sv.animate()        

        # with SceneVisualizer(s.peds, s, exp.plot_path) as sv:
        #     sv.plot()
except Exception as e:
    file_finder.summary_to_json(idx, force_idx, False)
    print("error during simulation")
    print(e)
    




    

