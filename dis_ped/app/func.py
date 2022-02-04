import json
from msilib.schema import File
import os
from dis_ped.video.video_data import VideoData
from dis_ped.video.peds import Pedestrians
from dis_ped.app.filefinder import FileFinder

class Experiment(object):
    def __init__(self, config_path):
        with open(config_path, 'r', encoding="UTF-8") as f:
            self.cfg = json.load(f)
        
        self.file_finder = FileFinder(config_path)
        self.idx = 0
        self.force_idx = 0

    @property
    def video(self) -> VideoData:
        try:
            hp_path = self.file_finder.hp_path(self.idx)
            vp_path = self.file_finder.vp_path(self.idx)        
            v = VideoData(hp_path, vp_path, self.idx)
        except FileNotFoundError:
            hp_path = self.file_finder.hp_path_2(self.idx)
            vp_path = self.file_finder.vp_path_2(self.idx)        
            v = VideoData(hp_path, vp_path, self.idx)            
        return v
        
    @property
    def peds(self):
        basic_path = self.file_finder.basic_path(self.idx)
        with open(basic_path, 'r') as f:
            json_data = json.load(f)
        return Pedestrians(json_data)

    @property
    def obstacle(self):
        return self.cfg["obstacles"]

    @property
    def simul_result_path(self):
        return self.file_finder.simul_result_path(self.idx, self.force_idx)

    @property
    def animation_path(self):
        return self.file_finder.animation_path(self.idx, self.force_idx)

    @property
    def plot_path(self):
        return self.file_finder.plot_path(self.idx, self.force_idx)

    @property
    def force_config(self):
        return self.cfg["forces"]

    @property
    def scene_config(self):
        return self.cfg["scene"]

    @property
    def simul_config(self):
        return self.cfg["condition"]

    def set_experiment(self, idx, force_idx):
        self.idx = idx
        self.force_idx = force_idx
        self.set_folder_path()
    
    def save_vid_data(self):
        basic_path = self.file_finder.basic_path(self.idx)
        gt_path = self.file_finder.gt_path(self.idx)
        self.video.to_json(basic_path)        
        self.video.trajectory_to_json(gt_path)
        return

    def set_folder_path(self):
        env_path = self.file_finder.env_path(self.idx)
        force_path= self.file_finder.force_path(self.idx, self.force_idx)
        if not os.path.exists(env_path):
            os.mkdir(env_path)

        if not os.path.exists(force_path):
            os.mkdir(force_path)      
