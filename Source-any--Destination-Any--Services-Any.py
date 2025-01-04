import pandas as pd
import re
from tabulate import tabulate

# Correct path to your Excel file
file_path = 'modified_firewall_updated.xlsx'

# Load the Excel file and handle errors
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit(1)
except Exception as e:
    print(f"Error loading the Excel file: {e}")
    exit(1)

# Normalize values to lowercase and treat 'any' and empty values as 'any'
def normalize_value(value):
    if isinstance(value, str):
        # Strip out anything inside square brackets and then check for 'any'
        value = re.sub(r'\[.*?\]', '', value).strip().lower()
        # If the value contains 'any' or is empty, treat it as 'any'
        if 'any' in value or value == '':
            return 'any'
    return value

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    source = normalize_value(row.get('Source', ''))
    destination = normalize_value(row.get('Destination', ''))
    service = normalize_value(row.get('Service', ''))

    # Check if all are 'any'
    if source == 'any' and destination == 'any' and service == 'any':
        results.append({
            "Row Number": index + 2,  # Adjust for 1-based index and header row
            "Rule Name": row.get('Rule', 'N/A'),
            "Source": source,
            "Destination": destination,
            "Service": service,
        })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)

# Print results to the console with formatting
if not results_df.empty:
    print("\nMatching Rules (Source: any, Destination: any, Service: any):")
    print(tabulate(results_df, headers='keys', tablefmt='pretty', showindex=False))
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-any--Destination-Any--Services-Any.xlsx'
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
