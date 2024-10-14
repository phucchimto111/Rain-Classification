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
    # Extract the base name (file name without path)
    base_name = os.path.basename(filename)

    # Regex patterns for both formats, updated to account for an optional suffix like _TB
    pattern1 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})[_A-Z]*\.tif$')
    pattern2 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})\.Z([0-9]{2})([0-9]{2})[_A-Z]*\.tif$')

    # Try matching the first pattern (VAR_YYYYMMDDHHMMSS.tif)
    match1 = pattern1.search(base_name)
    if match1:
        year, month, day, hour, minute, second = match1.groups()
        return {
            'year': int(year), 
            'month': int(month), 
            'day': int(day),
            'hour': int(hour), 
            'minute': int(minute), 
            'second': int(second)
        }

    # Try matching the second pattern (VAR_YYYYMMDD.ZHHMM.tif)
    match2 = pattern2.search(base_name)
    if match2:
        year, month, day, hour, minute = match2.groups()
        return {
            'year': int(year), 
            'month': int(month), 
            'day': int(day),
            'hour': int(hour), 
            'minute': int(minute), 
            'second': None  # No seconds in this format
        }

    # If no pattern matches, raise an exception or return None
    raise ValueError(f"Filename format not recognized: {filename}")


def process_tif_files(tif_files, output_csv):
    data = []
    
    for tif_file in tif_files:
        # Open the .tif file with rasterio
        with rasterio.open(tif_file) as dataset:
            # Read the file as a 2D array (band 1)
            band = dataset.read(1)
            
            # Get the affine transformation to convert pixel indices to coordinates
            transform = dataset.transform
            
            # Iterate over each pixel (row, col) in the 2D array
            for row in range(band.shape[0]):
                for col in range(band.shape[1]):
                    value = band[row, col]
                    
                    # Convert value is None, NaN, -inf, or -9999 to 0
                    if value is None or np.isnan(value) or np.isinf(value) or value == -9999:
                        value = 0 
                    
                    # Get the X, Y coordinates of the pixel
                    x, y = rasterio.transform.xy(transform, row, col)

                    # Get datetime
                    date_data = extract_datetime_from_tif(tif_file)

                    year = date_data['year']
                    month = date_data['month']
                    day = date_data['day']
                    hour = date_data['hour']
                    
                    # Define label if file is Radar
                    label = 1 if value > 0 else 0
                    
                    # Append the result to the data list
                    data.append([x, y, row, col, value, year, month, day, hour, label])
    
    # Convert to a pandas DataFrame
    df = pd.DataFrame(data, columns=['X', 'Y', 'row', 'col', 'value', 'year', 'month', 'day', 'hour', 'label'])
    
    # Save DataFrame to CSV
    df.to_csv(output_csv, index=False)
    print(f"CSV saved: {output_csv}")

def main():
    # print(len(list_tif_files_recursively("../DATA/Radar/2019/04/01/")))
    # print(list_tif_files_recursively("../DATA/HIMA/B04B/2019/04/01/"))
    # print(extract_datetime_from_tif("../DATA/HIMA/B04B/2019/04/04/B04B_20190404.Z0000_TB.tif"))
    # print(extract_datetime_from_tif("../DATA/Radar/2019/04/04/Radar_20190404210000.tif"))
    # print(list_folders("../DATA/HIMA/"))
    output_csv = "test.csv"
    print(process_tif_files(["../DATA/Radar/2019/04/01/Radar_20190401130000.tif"], output_csv))
    

if __name__ == "__main__":
    main()
