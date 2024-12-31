import os
import pandas as pd

def convert_csv_to_xlsx(folder_path, new_file_name):
    # List all files in the directory
    for file_name in os.listdir(folder_path):
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            # Construct full file path
            csv_file_path = os.path.join(folder_path, file_name)
            # Read the CSV file
            df = pd.read_csv(csv_file_path)
            # Define the new XLSX file path
            xlsx_file_path = os.path.join(folder_path, new_file_name)
            # Save the DataFrame to an XLSX file
            df.to_excel(xlsx_file_path, index=False)
            # Delete the original CSV file
            os.remove(csv_file_path)
            print(f"Converted and renamed '{file_name}' to '{new_file_name}' in '{folder_path}'")
            break  # Exit after processing the first CSV file

# Define the folder paths
fw_folder = 'FW'
address_objects_folder = 'Address Objects'

# Convert and rename files in the specified folders
convert_csv_to_xlsx(fw_folder, 'firewall.xlsx')
convert_csv_to_xlsx(address_objects_folder, 'rules.xlsx')
