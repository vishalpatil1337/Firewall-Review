import os
import pandas as pd

def convert_csv_to_xlsx(folder_path, new_file_name):
    # List all files in the directory
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    # Process CSV files first
    if csv_files:
        # Read the first CSV file
        csv_file_name = csv_files[0]
        csv_file_path = os.path.join(folder_path, csv_file_name)
        df = pd.read_csv(csv_file_path)
        
        # Define the new XLSX file path
        xlsx_file_path = os.path.join(folder_path, new_file_name)
        
        # Save the DataFrame to an XLSX file
        df.to_excel(xlsx_file_path, index=False)
        
        # Delete the original CSV file
        os.remove(csv_file_path)
        print(f"Converted and renamed '{csv_file_name}' to '{new_file_name}' in '{folder_path}'")
    
    # If no CSV files, but Excel files exist
    elif xlsx_files:
        # Rename the first Excel file if it's not already named as specified
        for excel_file in xlsx_files:
            if excel_file != new_file_name:
                old_excel_path = os.path.join(folder_path, excel_file)
                new_excel_path = os.path.join(folder_path, new_file_name)
                os.rename(old_excel_path, new_excel_path)
                print(f"Renamed existing Excel file '{excel_file}' to '{new_file_name}' in '{folder_path}'")
                break
    else:
        print(f"No CSV or Excel files found in '{folder_path}'")

# Define the folder paths
fw_folder = 'FW'
address_objects_folder = 'Address Objects'

# Convert and rename files in the specified folders
convert_csv_to_xlsx(fw_folder, 'firewall.xlsx')
convert_csv_to_xlsx(address_objects_folder, 'rules.xlsx')
