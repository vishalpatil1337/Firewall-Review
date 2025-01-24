import pandas as pd
import os

# Check if the file exists
file_path = 'output_external_internal.xlsx'
if not os.path.exists(file_path):
    print("File 'output_external_internal.xlsx' not found.")
else:
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=None)

    # Extract the sheet names and work on the first sheet
    sheet_name = list(df.keys())[0]
    df_sheet = df[sheet_name]

    # Print the first few rows to check the column names
    print("First few rows of the sheet:")
    print(df_sheet.head())

    # Check if the columns are named correctly (e.g., "Rule Type" and "Row Number")
    if 'Rule Type' in df_sheet.columns and 'Row Number' in df_sheet.columns:
        # Create a dictionary to track seen values in column "Row Number"
        seen_values = {}
        
        # Iterate through the rows
        for index, row in df_sheet.iterrows():
            col_a_value = row['Rule Type']
            col_b_value = row['Row Number']
            
            # If the value in column B is already seen
            if col_b_value in seen_values:
                # Modify the first occurrence of the value in column A
                first_index = seen_values[col_b_value]
                df_sheet.at[first_index, 'Rule Type'] = df_sheet.at[first_index, 'Rule Type'] + " - " + col_a_value
                # Remove the second occurrence
                df_sheet = df_sheet.drop(index)
            else:
                # Otherwise, store the index of the first occurrence
                seen_values[col_b_value] = index

        # Save the modified DataFrame back to a new sheet in the Excel file
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Write original sheet
            df[sheet_name].to_excel(writer, index=False, sheet_name=sheet_name)
            # Write modified sheet
            df_sheet.to_excel(writer, index=False, sheet_name='Modified_Sheet')

        print("File updated successfully and saved to 'Modified_Sheet'.")
    else:
        print("Columns 'Rule Type' and 'Row Number' not found in the sheet.")
