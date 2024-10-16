from helper import *

output = "../output/radar.csv"
tif_files = list_tif_files_recursively("../../TEST_DATA/Radar/2019/04/01/")
tif_to_csv(tif_files, output)
