import pandas as pd
import os

# Check if the file exists
file_path = 'firewall_analysis_results.xlsx'
if not os.path.exists(file_path):
    print("File 'firewall_analysis_results.xlsx' not found.")
else:
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=None)

    # Extract the sheet names and work on the first sheet
    sheet_name = list(df.keys())[0]
    df_sheet = df[sheet_name]

    # Print the first few rows to check the column names
    print("First few rows of the sheet:")
    print(df_sheet.head())

    # Check if the columns are named correctly (e.g., "Type" and "Excel Row")
    if 'Type' in df_sheet.columns and 'Excel Row' in df_sheet.columns:
        # Create a dictionary to track seen values in column "Excel Row"
        seen_values = {}
        
        # Iterate through the rows
        for index, row in df_sheet.iterrows():
            col_a_value = row['Type']
            col_b_value = row['Excel Row']
            
            # If the value in column B is already seen
            if col_b_value in seen_values:
                # Modify the first occurrence of the value in column A
                first_index = seen_values[col_b_value]
                df_sheet.at[first_index, 'Type'] = df_sheet.at[first_index, 'Type'] + " - " + col_a_value
                # Remove the second occurrence
                df_sheet = df_sheet.drop(index)
            else:
                # Otherwise, store the index of the first occurrence
                seen_values[col_b_value] = index

        # Save the modified DataFrame back to the Excel file
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df_sheet.to_excel(writer, index=False, sheet_name=sheet_name)

        print("File updated successfully.")
    else:
        print("Columns 'Type' and 'Excel Row' not found in the sheet.")
