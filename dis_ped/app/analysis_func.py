from distutils.command.config import config
import json
import os
from dis_ped.app.func import Experiment

class Analysis(object):
    def __init__(self, config_path):           
        with open(config_path, 'r') as f:
            self.cfg = json.load(f)
        self.exp = Experiment(config_path)
        self.idx = 0
        self.force_idx = 0
    
    def set_analysis(self, idx):
        self.exp.set_folder_path()
        self.idx = idx

    
        