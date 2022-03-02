import json
from dis_ped.result.vid_result import VidResult

class Analysis(object):
    def __init__(self, compare_idx_path):
        with open(compare_idx_path, "r", encoding="UTF-8") as f:
            data = json.load(f)

        self.vid_result_dict = {}
        for vid_idx, result_dict in data["result"].items():
            vid_res = VidResult(result_dict)
            self.vid_result_dict[vid_idx] = vid_res

    def average_ade(self):
        return
    
    def average_ade_standard(self, threshold):
        return    

    def average_dtw(self):
        return
    
    def average_dtw_standard(self, threshold):
        return    

    def average_social(self):
        return
    
    def average_social_standard(self, threshold):
        return