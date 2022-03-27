import os
from dis_ped.config.filefinder import FileFinder
import sys

setting_folder = sys.argv[1]

setting_path_list = []
for path, dirs, files in os.walk(setting_folder):
    for file in files:
        if file.split(".")[-1] == "json":
            setting_path_list.append(os.path.join(path, file))


for set_idx, setting_path in enumerate(setting_path_list):
    finder = FileFinder(setting_path)
    print("start")
    vid_folder_list = finder.get_vid_folder_list()
    total = len(vid_folder_list)

    for progress_idx, folder_path in enumerate(vid_folder_list):
        idx = folder_path.split("\\")[-1]
        os.system("python app_simulate.py "+idx+" "+setting_path)
        os.system("python app_validate.py "+idx+" "+setting_path)
        print(str(progress_idx)+"/"+str(total), str(set_idx)+"/"+str(len(setting_path_list)))

    os.system("python app_compare.py " + setting_path)
    os.system("python app_aggregate.py " + setting_path)