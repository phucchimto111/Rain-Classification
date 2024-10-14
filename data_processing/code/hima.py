from ultils import *

hima_sub_folder = [folder for folder in list_folders("../../TEST_DATA/HIMA/")]

for band in hima_sub_folder: 
    print(band)
    band_path = f"{band}/2019/04/01"
    output_csv = f"{band.split("/")[3]}hima.csv"
    tif_files = list_tif_files_recursively(band_path)
    process_tif_files(tif_files, output_csv)
#    output_csv = f"{band}_hima.csv"
#    tif_files = list_tif_files_recursively(band)
#    process_tif_files(tif_files, output_csv)
