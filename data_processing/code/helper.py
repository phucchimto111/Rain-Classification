import os
import re
import numpy as np
import pandas as pd
import rasterio

def list_tif_files_recursively(path):
    tif_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.tif'):
                tif_files.append(os.path.join(dirpath, filename))
    tif_files.sort()
    return tif_files

def list_folders(path):
    folders = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    folders.sort()
    return folders

def extract_datetime_from_tif(filename):
    """Extract date-time information from the filename."""
    base_name = os.path.basename(filename)
    pattern1 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})[_A-Z]*\.tif$')
    pattern2 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})\.Z([0-9]{2})([0-9]{2})[_A-Z]*\.tif$')

    match1 = pattern1.search(base_name)
    if match1:
        year, month, day, hour, *_ = match1.groups()
        return int(year), int(month), int(day), int(hour)

    match2 = pattern2.search(base_name)
    if match2:
        year, month, day, hour, _ = match2.groups()
        return int(year), int(month), int(day), int(hour)

    raise ValueError(f"Filename format not recognized: {filename}")

def tif_to_csv(tif_files, output_csv):
    """Process .tif files and save the results as a CSV."""
    data = []

    for tif_file in tif_files:
        var_name = get_var_from_path(tif_file)

        with rasterio.open(tif_file) as dataset:
            band = dataset.read(1).flatten()  # Flatten the 2D array into 1D for faster processing
            rows, cols = np.indices(dataset.shape).reshape(2, -1)  # Generate row and col indices
            
            # Replace invalid values (None, NaN, -inf, -9999) with 0
            band = np.where(np.isnan(band) | np.isinf(band) | (band == -9999), 0, band)

            year, month, day, hour = extract_datetime_from_tif(tif_file)

            # Create labels only for "Radar" files
            if var_name == "Radar":
                labels = (band > 0).astype(int)  # 1 if value > 0, else 0
                data.extend(zip(rows, cols, [year]*len(band), [month]*len(band), 
                                [day]*len(band), [hour]*len(band), band, labels))
            else:
                data.extend(zip(rows, cols, [year]*len(band), [month]*len(band), 
                                [day]*len(band), [hour]*len(band), band))

    # Create DataFrame after the loop completes
    columns = ['row', 'col', 'year', 'month', 'day', 'hour', var_name]
    if 'Radar' in [get_var_from_path(f) for f in tif_files]:
        columns.append('label')

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_csv, index=False)
    print(f"CSV saved: {output_csv}")

def get_var_from_path(file_path):
    base_name = os.path.basename(file_path)
    var_name = base_name.split('_')[0]
    return var_name

if __name__ == "__main__":
    # print(extract_datetime_from_tif("../../TEST_DATA/HIMA/B06B/2020/10/10/B06B_20201010.Z0200_TB.tif"))
    # tif_to_csv(["../../TEST_DATA/HIMA/B06B/2020/04/04/B06B_20200404.Z0000_TB.tif"], "output.csv")
    # print(get_var_from_path("../../TEST_DATA/HIMA/B06B/"))
    pass
