import sys
import numpy as np
from dis_ped.video.result_data import ResultData
from dis_ped.config.filefinder import FileFinder
import matplotlib.pyplot as plt
from dis_ped.video.parameters import DataIndex as Index
from dis_ped.utils.stateutils import minmax
import os
from dis_ped.video.plots import PlotGenerator


idx = sys.argv[1]
force_idx = sys.argv[2]
file_path = sys.argv[3]

    
file_finder = FileFinder(file_path)
trajectory_path = file_finder.simul_result_path(idx, force_idx)
gt_path = file_finder.gt_path(idx)
valid_path = file_finder.valid_path(idx, force_idx)
result_data = ResultData(trajectory_path, gt_path)
valid_path = file_finder.valid_path(idx, force_idx)
pg = PlotGenerator(file_path, idx, force_idx)
pg.save_figs()



exit()

fig, ax = plt.subplots()

# fig setting
plt.rcParams['font.family'] = 'Times New Roman'
ax.grid(linestyle="dotted")
ax.set_aspect("equal")
ax.margins(2.0)
ax.set_axisbelow(True)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
plt.rcParams["animation.html"] = "jshtml"


# x, y limit from states, only for animation
margin = 2.0
# xy_limits = np.array(
#     [minmax(state) for state in self.states]
# )  # (x_min, y_min, x_max, y_max)
xy_limits = np.array(
    [result_data.minmax(person_idx) for person_idx in range(0, result_data.num_person)]
)
xy_min = np.min(xy_limits[:, :2], axis=0) - margin
xy_max = np.max(xy_limits[:, 2:4], axis=0) + margin
ax.set(xlim=(xy_min[0], xy_max[0]), ylim=(xy_min[1], xy_max[1]))


def is_visual(data_length, min_time, max_time):
    if max_time < data_length:
        return True, min_time, max_time
    elif min_time < data_length < max_time:
        return True, min_time, data_length
    else:
        return False, -1, -1

def generate_fig(min_time, max_time, data):
    for ped_id in range(0, data.num_person):
        states = data.origin_states[min_time:max_time,ped_id]
        px, py = states[:, Index.px.index], states[:, Index.py.index]
        visible = states[:, Index.visible.index] == 1

    if ped_id==0:
        line, = ax.plot(px[visible], py[visible],"-o", markersize=0.05, color="black")
        line_legend.append(line)
    else:
        ax.plot(px[visible], py[visible],"-o", markersize=0.05, color="black")

    for ped_id in range(0, data.num_person):
        states = data.gt_states[min_time:max_time,ped_id]
        px, py = states[:, Index.px.index], states[:, Index.py.index]
        visible = states[:, Index.visible.index] == 1
        if ped_id ==0:
            line, = ax.plot(px[visible], py[visible], label=f"ped gt", markersize=0.05, color="black", linestyle="--")
            line_legend.append(line)
        else:
            ax.plot(px[visible], py[visible], markersize=0.05, color="black", linestyle="--")

    ax.legend(line_legend, ["result", "gt"])
    return

# data
line_legend = []
time = max(result_data.gt_time, result_data.simulation_time)
repeat = time//50
for i in range(0, repeat):
    min_time = i * 50
    max_time = min_time + 50
    visual, min_time, max_time = is_visual(result_data.simulation_time)
    if visual:
        generate_fig(min_time, max_time, result_data)
        output = os.path.join(valid_path,"test"+str(min_time)+".png")



fig.savefig(output, dpi=300)


        

    
        

# print(result_data.gt_data)

