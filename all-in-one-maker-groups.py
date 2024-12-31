import pandas as pd
import os
import glob
import re

# Function to clean illegal characters from strings
def clean_string(s):
    if isinstance(s, str):
        # Remove illegal characters
        return re.sub(r'[^\x20-\x7E]', '', s)  # Keep only printable ASCII characters
    return s

# Function to extract the group name from the row
def extract_group_name(s):
    if isinstance(s, str):
        # Split the string and return the last part after the space
        parts = s.split()
        return parts[-1] if len(parts) > 1 else s
    return s

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the Groups folder
folder_path = os.path.join(script_dir, 'Groups')

# Create a list to hold DataFrames
dataframes = []

# Read all CSV files in the Groups folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Check if any CSV files were found
if not csv_files:
    print("No CSV files found in the 'Groups' directory.")
else:
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, header=None)
        # Clean the data in the DataFrame using apply with map
        df = df.apply(lambda col: col.map(clean_string))
        dataframes.append(df)

    # Concatenate all DataFrames into one
    all_data = pd.concat(dataframes, ignore_index=True)

    # Create a new DataFrame to hold the consolidated data
    consolidated_data = []

    # Group by the first column and concatenate the second column values
    for key, group in all_data.groupby(0):
        # Extract the group name from the key
        group_name = extract_group_name(key)
        consolidated_row = [group_name, ', '.join(group[1].astype(str))]
        consolidated_data.append(consolidated_row)

    # Create a DataFrame from the consolidated data
    final_df = pd.DataFrame(consolidated_data, columns=['Row A', 'Row B'])

    # Save the final DataFrame to an Excel file in the same directory as the script
    output_file = os.path.join(script_dir, 'all-in-one.xlsx')
    final_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Consolidated data saved to {output_file}")
