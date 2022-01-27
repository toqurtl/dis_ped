import os
import json


class FileFinder(object):
    def __init__(self, config_path):
        with open(config_path, 'r', encoding="UTF-8") as f:
            self.cfg = json.load(f)        

    @property
    def result_path(self):
        return self.cfg["path"]["result_folder_path"]

    @property
    def vid_path(self):
        return os.path.abspath(self.cfg["path"]["vid_folder_path"])

    @property
    def result_csv_path(self):
        return os.path.join(self.result_path, "result.csv")

    @property
    def simul_time_threshold(self):
        return int(self.cfg["condition"]["simul_time_threshold"])

    def env_path(self, idx):
        return os.path.join(self.result_path, str(idx))

    def basic_path(self, idx):
        return os.path.join(self.env_path(idx), "data.json")
    
    def gt_path(self, idx):
        return os.path.join(self.env_path(idx),"gt.json")

    def hp_path(self, idx):
        return os.path.join(self.vid_path, idx, "hp.csv")

    def hp_path_2(self, idx):
        return os.path.join(self.vid_path, idx, idx+"_hp.csv")
    
    def vp_path(self, idx):
        return os.path.join(self.vid_path, idx, "vp.csv")

    def vp_path_2(self, idx):
        return os.path.join(self.vid_path, idx, idx+"_vp.csv")

    def compare_path(self, idx):
        return os.path.join(self.env_path(idx), "compare.json")

    def force_path(self, idx, force_idx):
        return os.path.join(self.result_path, str(idx), str(force_idx))
    
    def summary_path(self, idx, force_idx):
        return os.path.join(self.force_path(idx, force_idx), "summary.json")

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

    def get_exp_folder_list(self):
        folder_list = []
        for element in os.listdir(self.result_path):
            element_path = os.path.join(self.result_path, element)
            if os.path.isdir(element_path):
                folder_list.append(element_path)
        return folder_list

    def get_vid_folder_list(self):
        folder_list = []        
        for element in os.listdir(self.vid_path):
            element_path = os.path.join(self.vid_path, element)
            if os.path.isdir(element_path):                
                folder_list.append(element_path)                
        return folder_list

    def summary_to_json(self, idx, force_idx, success):
        data = {}
        data["success"] = success
        
        with open(self.summary_path(idx, force_idx), 'w') as f:
            json.dump(data, f, indent=4)
        return

    def get_compare_json_path_list(self):
        path_list = []
        for element in os.listdir(self.result_path):
            element_path = os.path.join(self.result_path, element)
            compare_json_path = os.path.join(element_path, "compare.json")
            if os.path.isdir(element_path) and os.path.exists(compare_json_path):
                path_list.append(compare_json_path)
        return path_list

    def is_comparable(self, idx):
        folder_list = self.get_force_folder_list(idx)
        if len(folder_list) < 1:
            return False
        for folder_path in folder_list:
            force_idx = folder_path.split("\\")[-1]
            with open(self.summary_path(idx, force_idx),"r",encoding="UTF-8") as f:
                success = bool(json.load(f)["success"])
            if not success:
                return False
        return True

    def is_success(self, idx):
        if not os.path.exists(self.compare_path(idx)):
            return False
        with open(self.compare_path(idx), "r", encoding="UTF-8") as f:
            success = bool(json.load(f)["state"]["success"])
        return success
    