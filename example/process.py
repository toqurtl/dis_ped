import os
from dis_ped.app.filefinder import FileFinder

finder = FileFinder("setting_2.json")

print("start")

vid_folder_list = finder.get_vid_folder_list()
total = len(vid_folder_list)
print("force 0")
for num, vid_folder_path in enumerate(vid_folder_list):
    idx = vid_folder_path.split("\\")[-1]
    os.system("python app_simulate.py "+idx+" 0")
    print("force 0: (", str(num), "/", str(total), ")")
    os.system("python app_validate.py "+idx+" 0")
print("force 1")
for num, vid_folder_path in enumerate(vid_folder_list):
    idx = vid_folder_path.split("\\")[-1]
    os.system("python app_simulate.py "+idx+" 1")
    os.system("python app_validate.py "+idx+" 1")
    print("force 1: (", str(num), "/", str(total), ")")
print("force 2")
for num, vid_folder_path in enumerate(vid_folder_list):
    idx = vid_folder_path.split("\\")[-1]
    os.system("python app_simulate.py "+idx+" 2")
    os.system("python app_validate.py "+idx+" 2")
    print("force 2: (", str(num), "/", str(total), ")")


result_folder_list = finder.get_exp_folder_list()
total = len(result_folder_list)
for num, result_folder_path in enumerate(result_folder_list):
    idx = result_folder_path.split("\\")[-1]
    os.system("python app_compare.py "+idx)
    print("(", str(num), "/", str(total), ")")
    
os.system("python app_aggregate.py")
