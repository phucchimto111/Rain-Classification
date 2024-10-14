from ultils import *

era_sub_folder = [folder for folder in list_folders("../../TEST_DATA//ERA5/")]

for folder in era_sub_folder:
    print(folder)
    folder_path = f"{folder}/2019/04/01/"
    output_csv = f"{folder.split("/")[3]}era5.csv"
    tif_files = list_tif_files_recursively(folder_path)
    process_tif_files(tif_files, output_csv)
