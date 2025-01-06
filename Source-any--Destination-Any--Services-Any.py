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

# Function to check if a value is considered 'any'
def is_any(value):
    if isinstance(value, str):
        # Strip out anything inside square brackets and then check for 'any'
        stripped_value = re.sub(r'$$.*?$$', '', value).strip().lower()
        # If the value contains 'any' or is empty, treat it as 'any'
        return 'any' in stripped_value or stripped_value == ''
    return False

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    source = row.get('Source', '')
    destination = row.get('Destination', '')
    service = row.get('Service', '')

    # Check if all are 'any'
    if is_any(source) and is_any(destination) and is_any(service):
        results.append({
            "Row Number": index + 2,  # Adjust for 1-based index and header row
            "Rule Name": row.get('Rule', 'N/A'),  # Assuming there's a 'Rule' column
            "Source": source,
            "Destination": destination,
            "Service": service,
        })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)

# Print results to the console with formatting
if not results_df.empty:
    print("\nMatching Rules (Source: any, Destination: any, Service: any):")
    print(tabulate(results_df, headers='keys', tablefmt='fancy_grid', showindex=False))
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-any--Destination-Any--Services-Any.xlsx'
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
