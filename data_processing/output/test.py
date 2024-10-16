import pandas as pd
import glob
import os

# Directory where your CSV files are located
input_dir = "./csv/"
output_file = "combined_dataset.csv"

# Load radar.csv to keep its order
radar_df = pd.read_csv(os.path.join(input_dir, "radar.csv"))

# Get a list of all CSV files in the directory, excluding radar.csv
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
csv_files = [file for file in csv_files if "radar.csv" not in file]

# Initialize an empty DataFrame to hold the merged results
combined_df = radar_df.copy()

# Iterate through the additional CSV files
for file in csv_files:
    df = pd.read_csv(file)
    
    # Identify the value column (the last column in the CSV)
    value_column = df.columns[-1]  # Get the last column name

    # Merge on row, col, year, month, day, hour
    combined_df = pd.merge(
        combined_df,
        df[["row", "col", "year", "month", "day", "hour", value_column]],
        on=["row", "col", "year", "month", "day", "hour"],
        how="left",  # Use left join to keep all data from radar_df
    )

# Fill missing values with 0
combined_df = combined_df.fillna(0)

# Move the new value columns right before the label column
# Identify the last column (label)
label_column = 'label'

# Create a new DataFrame to re-arrange columns
value_columns = [col for col in combined_df.columns if col != label_column and col not in radar_df.columns]
new_column_order = list(combined_df.columns[:combined_df.columns.get_loc(label_column)]) + value_columns + [label_column]

# Reorder DataFrame
combined_df = combined_df[new_column_order]

# Save the final combined dataset to a CSV file
combined_df.to_csv(output_file, index=False)
print(f"Combined dataset saved to {output_file}")

