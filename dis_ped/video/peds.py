from typing import Dict, List
import numpy as np
from .ped import PedAgent
from .parameters import DataIndex as Index

class Pedestrians(object):
    def __init__(self, json_data):
        self.peds: Dict[int, PedAgent] = {}
        self.states: List[np.ndarray] = []
        self.group_states = []
        self._initialize(json_data)
    
    def _initialize(self, json_data):
        initial_state = []        
        for key, agent_data in json_data["initial_state"].items():            
            ped_info = json_data["ped_info"][key]
            ped = PedAgent(agent_data, ped_info)
            self.peds[int(key)] = ped
            initial_state.append(ped.current_state)        
        self.states.append(np.array(initial_state))
        self.group_states.append([])
        return
    
    @property
    def time_step(self):
        return len(self.states) - 1    

    @property
    def current_state(self):
        return self.states[-1]

    def state_at(self, time_step):
        return self.states[time_step]

    def update(self, new_peds_state, next_group_state, time_step):
        new_state_list = []
        for ped in self.peds.values():
            new_state = ped.update(new_peds_state)            
            new_state_list.append(new_state)                        
        if next_group_state is None:
            self.group_states.append([])
        else:    
            self.group_states.append(next_group_state)
        self.states.append(np.array(new_state_list))            
        return

    def check_finished(self):
        finish_state = self.current_state[:, Index.finished.index]    
        return np.sum(finish_state) == len(self.peds)

    def target_pos(self):
        gx_list, gy_list = [], []
        for idx, ped in self.peds.items():
            gx_list.append(ped.gx)
            gy_list.append(ped.gy)
        return np.array(gx_list), np.array(gy_list)

    def update_target_pos(self):
        gx_array, gy_array = self.target_pos()        
        self.current_state[:, Index.gx.index] = gx_array
        self.current_state[:, Index.gy.index] = gy_array
        return
