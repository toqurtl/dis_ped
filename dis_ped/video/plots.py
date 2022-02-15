from dis_ped.config.filefinder import FileFinder
from dis_ped.video.result_data import ResultData
from typing import List
from dis_ped.video.parameters import DataIndex as Index
import matplotlib.pyplot as plt
import numpy as np

import os
import json

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams["animation.html"] = "jshtml"


class PlotGenerator(object):
    def __init__(self, file_path, idx):
        self.finder = FileFinder(file_path)
        trajectory_path = self.finder.simul_result_path(idx)
        gt_path = self.finder.gt_path(idx)
        self.save_path = self.finder.env_path(idx)
        self.result_data = ResultData(trajectory_path, gt_path)
        self.line_legend = []
        with open(file_path, 'r', encoding="UTF-8") as f:
            config = json.load(f)
            self.resolution = config["scene"]["resolution"]
            self.obstacles = config["obstacles"]
            

    @property
    def obstacles(self) -> List[np.ndarray]:
        """obstacles is a list of np.ndarray"""
        return self._obstacles

    @obstacles.setter
    def obstacles(self, obstacles):
        """Input an list of (startx, endx, starty, endy) as start and end of a line"""
        if obstacles is None:
            self._obstacles = []
        else:
            self._obstacles = []
            for startx, endx, starty, endy in obstacles:
                samples = int(np.linalg.norm((startx - endx, starty - endy)) * self.resolution)
                line = np.array(
                    list(
                        zip(np.linspace(startx, endx, samples), np.linspace(starty, endy, samples))
                    )
                )
                self._obstacles.append(line)

    @property
    def origin_states(self):
        return self.result_data.origin_states

    @property
    def gt_states(self):
        return self.result_data.gt_states

    @property
    def simulation_length(self):
        return self.result_data.simulation_time

    @property
    def gt_length(self):
        return self.result_data.gt_time

    @property
    def num_person(self):
        return self.result_data.num_person

    def plot_obstacles(self, ax):
        for s in self.obstacles:            
            ax.plot(s[:, 0], s[:, 1], "-o", color="black", markersize=0.5)
        return ax

    def _is_visual(self, data_length, min_time, max_time):
        if max_time <= data_length:
            return True, min_time, max_time
        elif min_time <= data_length < max_time:
            return True, min_time, data_length
        else:
            return False, -1, -1

    def generate_plots(self):
        fig, ax = plt.subplots()        
        ax.grid(linestyle="dotted")
        ax.set_aspect("equal")
        ax.margins(2.0)
        ax.set_axisbelow(True)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        margin = 2.0
        xy_limits = np.array(
            [self.result_data.minmax(person_idx) for person_idx in range(0, self.result_data.num_person)]
        )
        xy_min = np.min(xy_limits[:, :2], axis=0) - margin
        xy_max = np.max(xy_limits[:, 2:4], axis=0) + margin
        ax.set(xlim=(xy_min[0], xy_max[0]), ylim=(xy_min[1], xy_max[1]))
        return fig, ax

    def simulation_plotting(self, min_time, max_time, ax):
        line_legend = []        
        for ped_id in range(0, self.num_person):
            states = self.origin_states[min_time:max_time,ped_id]
            px, py = states[:, Index.px.index], states[:, Index.py.index]
            visible = states[:, Index.visible.index] == 1
            line, = ax.plot(px[visible], py[visible],"-o", markersize=0.05, color="black")
            ax.plot(px[visible], py[visible],"-o", markersize=0.05, color="black")
        return ax

    def gt_plotting(self, min_time, max_time, ax):
        for ped_id in range(0, self.num_person):
            states = self.gt_states[min_time:max_time,ped_id]
            px, py = states[:, Index.px.index], states[:, Index.py.index]
            visible = states[:, Index.visible.index] == 1
            line, = ax.plot(px[visible], py[visible], markersize=0.05, color="black", linestyle="--")
        return ax

    def save_figs(self):        
        num_fig = max(self.gt_length, self.simulation_length) // 50 + 1        
        for i in range(0, num_fig):
            fig, ax = self.generate_plots()
            min_step, max_step = i * 50, (i+1)*50            
            visual, min_time, max_time = self._is_visual(self.simulation_length, min_step, max_step)            
            if visual:
                ax = self.simulation_plotting(min_time, max_time, ax)                
            
            visual, min_time, max_time = self._is_visual(self.gt_length, min_step, max_step)            
            if visual:
                ax = self.gt_plotting(min_time, max_time, ax)
            ax = self.plot_obstacles(ax)          
            output_path = os.path.join(self.save_path, "trajectory_"+str(min_step)+".png")
            fig.savefig(output_path, dpi=300)
        

        