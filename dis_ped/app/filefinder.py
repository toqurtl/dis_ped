import os
import json


class FileFinder(object):
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.cfg = json.load(f)        

    @property
    def result_path(self):
        return self.cfg["path"]["result_folder_path"]

    @property
    def vid_path(self):
        return os.path.abspath(self.cfg["path"]["vid_folder_path"])
    
    def env_path(self, idx):
        return os.path.join(self.result_path, str(idx))

    def basic_path(self, idx):
        return os.path.join(self.env_path(idx), "data.json")
    
    def gt_path(self, idx):
        return os.path.join(self.env_path(idx),"gt.json")

    def hp_path(self, idx):
        return os.path.join(self.vid_path, idx, "hp.csv")
    
    def vp_path(self, idx):
        return os.path.join(self.vid_path, idx, "vp.csv")

    def compare_path(self, idx):
        return os.path.join(self.env_path(idx), "compare.json")

    def force_path(self, idx, force_idx):
        return os.path.join(self.result_path, str(idx), str(force_idx))

    def plot_path(self, idx, force_idx):
        return os.path.join(self.force_path(idx, force_idx), "plot")

    def animation_path(self, idx, force_idx):
        return os.path.join(self.force_path(idx, force_idx), "animation")

    def simul_result_path(self, idx, force_idx):
        return os.path.join(self.force_path(idx, force_idx), "result.json")
    
    def valid_path(self, idx, force_idx):
        return os.path.join(self.force_path(idx, force_idx), "valid.json")
    
    def get_force_folder_list(self, idx):
        path = self.env_path(idx)
        force_folder_list = []
        for element in os.listdir(path):
            element_path = os.path.join(path, element)
            if os.path.isdir(element_path):
                force_folder_list.append(element)
        return force_folder_list