import json
import numpy as np
from dis_ped.video.parameters import DataIndex as Index
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw


def get_distance(data, p_idx_1, p_idx_2):
    px_1, py_1 = data[p_idx_1][Index.px.index], data[p_idx_1][Index.py.index]
    px_2, py_2 = data[p_idx_2][Index.px.index], data[p_idx_2][Index.py.index]
    return ((px_1-px_2)**2 + (py_1-py_2)**2)**0.5


class ResultData(object):
    def __init__(self, origin_path, gt_path):
        with open(origin_path, 'r') as f:
            self.origin_data = json.load(f)
        
        with open(gt_path, 'r') as f:
            self.gt_data = json.load(f)

        self.origin_states = \
            np.array([data["states"] for data in self.origin_data.values()])
        
        self.gt_states = \
            np.array([data["states"] for data in self.gt_data.values()])

        return

    @property
    def num_person(self):
        return len(self.origin_states[0])
        
    def ade_range(self, person_idx):        
        origin_person_data = self.origin_states[:, person_idx]
        gt_person_data = self.gt_states[:, person_idx]
        start = origin_person_data[0][Index.start_time.index]
        origin_finish = len(origin_person_data)
        gt_finish = len(gt_person_data)

        for idx, data in enumerate(origin_person_data):                
            if data[Index.finished.index] == 1:               
                origin_finish = idx-1
                break
        
        for idx, data in enumerate(gt_person_data):                
            if data[Index.finished.index] == 1:               
                gt_finish = idx-1
                break
        finish = min(origin_finish, gt_finish)

        return int(start), int(finish)

    def ade_of_person(self, person_idx):
        origin_person_data = self.origin_states[:, person_idx]
        gt_person_data = self.gt_states[:, person_idx]
        start, finish = self.ade_range(person_idx)
        traj_x = origin_person_data[start:finish+1, Index.px.index] 
        traj_y = origin_person_data[start:finish+1, Index.py.index]
        
        gt_x = gt_person_data[start:finish+1, Index.px.index]
        gt_y = gt_person_data[start:finish+1, Index.py.index]
        
        try:        
            d_x = np.sum(traj_x - gt_x) / (finish-start + 1)
            d_y = np.sum(traj_y - gt_y) / (finish-start + 1)
        except ValueError:
            traj_x, traj_y = traj_x[:-1], traj_y[:-1]
            d_x = np.sum(traj_x - gt_x) / (finish-start + 1)
            d_y = np.sum(traj_y - gt_y) / (finish-start + 1)

        return (d_x**2 + d_y**2)**0.5
    
    def fde_of_person(self, person_idx):
        origin_person_data = self.origin_states[:, person_idx]
        gt_person_data = self.gt_states[:, person_idx]
        
        origin_finish = len(origin_person_data)
        gt_finish = len(gt_person_data)

        for idx, data in enumerate(origin_person_data):                
            if data[Index.finished.index] == 1:               
                origin_finish = idx-1
                break
        
        for idx, data in enumerate(gt_person_data):                
            if data[Index.finished.index] == 1:               
                gt_finish = idx-1
                break


        last_traj_x = origin_person_data[origin_finish, Index.px.index]
        last_traj_y = origin_person_data[origin_finish, Index.py.index]    
        gt_traj_x = gt_person_data[gt_finish-1, Index.px.index]
        gt_traj_y = gt_person_data[gt_finish-1, Index.py.index]
        
        return ((last_traj_x - gt_traj_x)**2 + (last_traj_y - gt_traj_y)**2)**0.5

    def ade_of_scene(self):
        ade_sum = 0
        for person_idx in range(0, self.num_person):
            ade_sum += self.ade_of_person(person_idx)
        return ade_sum / self.num_person

    def fde_of_scene(self):
        fde_sum = 0        
        for person_idx in range(0, self.num_person):
            fde_sum += self.fde_of_person(person_idx)
        return fde_sum / self.num_person

    def risk_index_of_person(self, person_idx, distance):
        start, finish = self.ade_range(person_idx)
        ctn = 0
        check_data = []
        for time in range(start, finish+1):
            data = self.origin_states[time]            
            for idx, person_data in enumerate(data):
                is_visible = person_data[Index.visible.index] == 1
                if idx is not person_idx and is_visible:
                    dis = get_distance(data, person_idx, idx)
                    if dis < distance:
                        ctn += 1
                        check_data.append(time)
        return ctn, finish-start + 1, check_data

    def risk_index_of_scene(self, distance):
        result_data = {}
        avg = 0
        for person_idx in range(0, self.num_person):        
            ctn, total_time, check_data = self.risk_index_of_person(person_idx, distance)
            avg += ctn / total_time
        return avg / self.num_person

    def dtw_of_person(self, person_idx):
        origin_person_data = self.origin_states[:, person_idx]
        gt_person_data = self.gt_states[:, person_idx]
        start, finish = self.ade_range(person_idx)
        traj_x = origin_person_data[start:finish+1, Index.px.index] 
        traj_y = origin_person_data[start:finish+1, Index.py.index]
        
        gt_x = gt_person_data[start:finish+1, Index.px.index]
        gt_y = gt_person_data[start:finish+1, Index.py.index]        
        
        try:        
            traj = np.column_stack((traj_x, traj_y))
            gt = np.column_stack((gt_x, gt_y))
            distance, path = fastdtw(traj, gt, dist=euclidean)

        except ValueError:
            traj_x, traj_y = traj_x[:-1], traj_y[:-1]
            traj = np.column_stack((traj_x, traj_y))
            gt = np.column_stack((gt_x, gt_y))
            distance, path = fastdtw(traj, gt, dist=euclidean)

        return distance

    def dtw_of_scene(self):
        dtw_sum = 0
        for person_idx in range(0, self.num_person):
            dtw_sum += self.dtw_of_person(person_idx)
        return dtw_sum / self.num_person

    def result(self, vid_id, force_id):
        data = {}
        data["basic"] = {}
        data["result"] = {}
        data["basic"]["vid_id"] = vid_id
        data["basic"]["num_person"] = self.num_person
        data["basic"]["gt_time"] = len(self.gt_data)        
        data["result"]["force_id"] = int(force_id)
        data["result"]["simulation_time"] = len(self.origin_data)
        data["result"]["ade"] = self.ade_of_scene()
        data["result"]["fde"] = 0
        data["result"]["dtw"] = self.dtw_of_scene()
        # TODO - 추후 목표 distance 설정

        data["result"]["social"] = self.risk_index_of_scene(2)
        return data

            
                    
    def to_json(self, file_path, vid_id, force_id):
        state = self.result(vid_id, force_id)
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=4)
        return
        

