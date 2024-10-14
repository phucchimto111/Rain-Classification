from ultils import *

output = "radar.csv"
tif_files = list_tif_files_recursively("../DATA/Radar/2019/04/01/")
process_tif_files(tif_files, output)
