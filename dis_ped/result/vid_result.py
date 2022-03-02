class VidResult(object):
    def __init__(self, result_dict):        
        self.result_dict = result_dict
        self.vid_id = result_dict["vid_info"]["vid_idx"]
    
    @property
    def vid_idx(self):
        return self.result_dict["vid_info"]["vid_idx"]

    @property
    def gt_time(self):
        return self.result_dict["vid_info"]["gt_time"]

    @property    
    def num_person(self):
        return self.result_dict["vid_info"]["num_person"]

    @property
    def social(self):
        return self.result_dict["vid_info"]["social"]

    @property
    def success(self):
        return self.result_dict["simul_result"]["success"]

    @property
    def simul_time(self):
        return self.result_dict["simul_result"]["simul_time"]
    
    @property
    def ade(self):
        return self.result_dict["simul_result"]["ade"]

    @property
    def dtw(self):
        return self.result_dict["simul_result"]["dtw"]

    @property
    def social(self):
        return self.result_dict["simul_result"]["social"]

    @property
    def sdcr_error(self):
        return self.result_dict["simul_result"]["sdcr_error"]