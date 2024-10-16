from helper import *

hima_sub_folder = [folder for folder in list_folders("../../TEST_DATA/HIMA/")]

for band in hima_sub_folder: 
    specific_path = f"{band}/2019/04/01/"
    print(specific_path)

    tif_files = list_tif_files_recursively(specific_path) 
    tif_to_csv(tif_files, f"../output/Hima_{get_var_from_path(tif_files[0])}.csv")
