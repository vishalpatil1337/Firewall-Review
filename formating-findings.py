import pandas as pd
import os

# File name
file_findings = "output_cde-oos-findings.xlsx"
output_file_findings = "output_cde-oos-findings.xlsx"  # Save back to the same file

# Function to process the findings.xlsx file
def process_findings():
    try:
        # Check if the file exists
        if not os.path.exists(file_findings):
            print(f"File '{file_findings}' not found.")
            return

        # Read the input Excel file
        df = pd.read_excel(file_findings)
        print("Columns in the findings file:", df.columns.tolist())

        # Required columns
        required_columns_findings = ['Type', 'Excel Row']
        if all(col in df.columns for col in required_columns_findings):
            seen = {}
            rows_to_remove = []

            for index, row in df.iterrows():
                b_value = row['Excel Row']
                if pd.isna(b_value):
                    continue
                if b_value in seen:
                    # Append the duplicate 'Type' to the existing entry
                    df.at[seen[b_value], 'Type'] += f" - {row['Type']}"
                    rows_to_remove.append(index)
                else:
                    seen[b_value] = index

            # Drop duplicate rows
            df.drop(rows_to_remove, inplace=True)

            # Save the modified DataFrame to a new sheet in the same Excel file
            with pd.ExcelWriter(output_file_findings, engine='openpyxl', mode='a') as writer:
                df.to_excel(writer, sheet_name='Processed Findings', index=False)
                print(f"Processed findings data saved to a new sheet 'Processed Findings' in '{output_file_findings}'.")
        else:
            print(f"Required columns {required_columns_findings} not found in the findings file.")

    except Exception as e:
        print(f"An error occurred while processing findings file: {e}")

# Process the findings file
process_findings()
