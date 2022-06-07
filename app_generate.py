import json
import os


def save_sfm_1(idx, distance):
    setting_id = "social_sfm_1_"+str(idx)    
    folder_path = "setting_folder\\0326\\Social-SFM-1"
    file_name = "social_sfm_1_"+str(idx)+".json"
    file_path = os.path.join(folder_path, file_name)
    sfm_1_dict = {
        "setting_id": "social_sfm_1_1",
        "repulsive_force": "my_force",
        "path":{
            "vid_folder_path": "C:\\Users\\toqurtl\\snucem\\exp\\whole",
            "result_folder_path": "C:\\Users\\toqurtl\\snucem\\exp\\result\\0326"
        },
        "obstacles":[
            [5.15, 5.15, -8, 16],
            [-1.44, -1.44, -10, -1.2], 
            [-1.44, -1.44, 0, 6], 
            [-1.44, -1.44, 7.2, 16],
            [-1.44, 0, 7.2, 7.2],
            [0, 0, 7.2, 8.2],
            [-1.44, 0, 8.2, 8.2],
            [-1.44, 0, 0, 0],
            [0, 0, 0, 1],
            [-1.44, 0, 1, 1]
        ],
        "scene":{
            "enable_group": True,
            "agent_radius": 0.35,
            "step_width": 0.65,
            "max_speed_multiplier": 1.1,
            "tau": 0.5,
            "resolution": 10
        },
        "forces":{
            "force_save": True,
            "set":{
                "desired_force":{
                    "factor": 1.0,
                    "relaxation_time": 0.5,
                    "goal_threshold": 0.2
                },
                "obstacle_force":{
                    "factor": 10.0,
                    "sigma": 0.2,
                    "threshold": 0.2
                },
                "my_force":{
                    "factor": 1,
                    "desired_distance": 1.1,
                    "alpha": 2000,
                    "beta": 0.08,
                    "lambda": 0.5
                }
            }        
        },
        "condition":{
            "simul_time_threshold": 1000
        }

    }

    sfm_1_dict["setting_id"] = setting_id
    sfm_1_dict["forces"]["set"]["my_force"]["desired_distance"] = distance

    with open(file_path, "w") as f:
        json.dump(sfm_1_dict, f, indent=4)


def save_sfm_2(idx, distance):
    setting_id = "social_sfm_2_"+str(idx)    
    folder_path = "setting_folder\\0326\\Social_SFM-2"
    file_name = "social_sfm_2_"+str(idx)+".json"
    file_path = os.path.join(folder_path, file_name)
    sfm_2_dict = {
        "setting_id": "social_sfm_2_1",
        "repulsive_force": "my_force_2",
        "path":{
            "vid_folder_path": "C:\\Users\\toqurtl\\snucem\\exp\\whole",
            "result_folder_path": "C:\\Users\\toqurtl\\snucem\\exp\\result\\0326"
        },
        "obstacles":[
            [5.15, 5.15, -8, 16],
            [-1.44, -1.44, -10, -1.2], 
            [-1.44, -1.44, 0, 6], 
            [-1.44, -1.44, 7.2, 16],
            [-1.44, 0, 7.2, 7.2],
            [0, 0, 7.2, 8.2],
            [-1.44, 0, 8.2, 8.2],
            [-1.44, 0, 0, 0],
            [0, 0, 0, 1],
            [-1.44, 0, 1, 1]
        ],
        "scene":{
            "enable_group": True,
            "agent_radius": 0.35,
            "step_width": 0.65,
            "max_speed_multiplier": 1.1,
            "tau": 0.5,
            "resolution": 10
        },
        "forces":{
            "force_save": True,
            "set":{
                "desired_force":{
                    "factor": 1.0,
                    "relaxation_time": 0.5,
                    "goal_threshold": 0.2
                },
                "obstacle_force":{
                    "factor": 10.0,
                    "sigma": 0.2,
                    "threshold": 0.2
                },
            "my_force_2":{
                "factor": 1,
                "desired_distance": 2,
                "small_alpha": 20,
                "alpha": 2000,
                "beta": 0.08,
                "lambda": 0.5
            }
            }        
        },
        "condition":{
            "simul_time_threshold": 1000
        }

    }

    sfm_2_dict["setting_id"] = setting_id
    sfm_2_dict["forces"]["set"]["my_force_2"]["desired_distance"] = distance

    with open(file_path, "w") as f:
        json.dump(sfm_2_dict, f, indent=4)

# save_sfm_1(25, 2.4)
# save_sfm_2(24, 1.8)
for idx in range(26, 35):
    distance = (idx-25)*0.2+2.4
    save_sfm_1(idx, distance)

for idx in range(25, 36):
    distance = (idx-25)*0.2+2
    save_sfm_2(idx, distance)