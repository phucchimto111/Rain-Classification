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
    # Extract the base name (file name without the path)
    base_name = os.path.basename(filename)

    # Updated regex patterns to ignore minutes and seconds
    pattern1 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})[0-9]{4}[_A-Z]*\.tif$')
    pattern2 = re.compile(r'_([0-9]{4})([0-9]{2})([0-9]{2})\.Z([0-9]{2})[0-9]{2}[_A-Z]*\.tif$')

    # Try matching the first pattern (VAR_YYYYMMDDHHMMSS.tif)
    match1 = pattern1.search(base_name)
    if match1:
        year, month, day, hour = match1.groups()
        return {
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'hour': int(hour)
        }

    # Try matching the second pattern (VAR_YYYYMMDD.ZHHMM.tif)
    match2 = pattern2.search(base_name)
    if match2:
        year, month, day, hour = match2.groups()
        return {
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'hour': int(hour)
        }

    # If no pattern matches, raise an exception or return None
    raise ValueError(f"Filename format not recognized: {filename}")

def extract_var_name(filename):
    """Extract the variable name from the filename before the first underscore."""
    base_name = os.path.basename(filename)
    return base_name.split('_')[0]  # Extracts 'VAR' from 'VAR_YYYYMMDD...'

def process_tif_files(tif_files, output_csv):
    data = []

    for tif_file in tif_files:
        # Extract the variable name (e.g., VAR) from the filename
        var_name = extract_var_name(tif_file)

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

                    # Convert invalid values (None, NaN, -inf, -9999) to 0
                    if value is None or np.isnan(value) or np.isinf(value) or value == -9999:
                        value = 0 

                    # Get the X, Y coordinates of the pixel
                    x, y = rasterio.transform.xy(transform, row, col)

                    # Get datetime from the filename
                    date_data = extract_datetime_from_tif(tif_file)
                    year, month, day, hour = (
                        date_data['year'], 
                        date_data['month'], 
                        date_data['day'], 
                        date_data['hour']
                    )

                    # Only add 'label' if the file name contains 'Radar'
                    label = 1 if 'Radar' in tif_file and value > 0 else 0

                    # Append the result to the data list
                    if 'Radar' in tif_file:
                        data.append([x, y, row, col, value, year, month, day, hour, label])
                    else:
                        data.append([x, y, row, col, value, year, month, day, hour])

    # Define column names based on whether 'Radar' files were processed
    columns = ['X', 'Y', 'row', 'col', var_name, 'year', 'month', 'day', 'hour']
    if any('Radar' in f for f in tif_files):
        columns.append('label')

    # Convert to a pandas DataFrame
    df = pd.DataFrame(data, columns=columns)

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
    print(process_tif_files(["../../TEST_DATA/Radar/2019/04/01/Radar_20190401130000.tif"], output_csv))
    

if __name__ == "__main__":
    main()
