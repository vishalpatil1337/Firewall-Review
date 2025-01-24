import pandas as pd
from prettytable import PrettyTable
import re

# Load the Excel file
file_path = 'modified_firewall_updated.xlsx'
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit()
except Exception as e:
    print(f"An error occurred while loading the Excel file: {e}")
    exit()

def normalize_value(value):
    """Normalize the value by converting to lowercase and removing extra whitespace"""
    return str(value).lower().strip()

def is_any_value(item):
    """
    Check if a single item represents 'any'
    Uses regex to match any text in brackets followed by 'any'
    """
    item = normalize_value(item)
    
    # Define patterns to match
    patterns = [
        '^any$',  # Exactly "any"
        r'^\[.*?\]\s*any$'  # Anything in brackets followed by "any"
    ]
    
    return any(re.match(pattern, item) for pattern in patterns)

def is_all_any(value):
    """
    Check if all values in the field represent 'any'
    Returns True if the field is empty, contains only 'any' values, or variations of 'any'
    """
    # Handle empty/NaN values
    if pd.isna(value) or str(value).strip() == '':
        return True
    
    # Convert the value to string and normalize newlines and semicolons
    value_str = str(value).replace(';', '\n')
    
    # Split into lines and filter out empty lines
    lines = [line.strip() for line in value_str.split('\n') if line.strip()]
    
    # If all lines are empty, consider it as "any"
    if not lines:
        return True
    
    # Check if ALL lines are "any" values
    return all(is_any_value(line) for line in lines)

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    source = str(row['Source'])
    destination = str(row['Destination'])
    service = str(row['Service'])
    
    # Check conditions: All fields must be 'any'
    if is_all_any(source) and is_all_any(destination) and is_all_any(service):
        results.append({
            "Row Number": index + 2,
            "Rule Name": row.get('Rule', 'N/A'),
            "Source": source,
            "Destination": destination,
            "Service": service,
        })

# Print results to the console with formatting
if results:
    table = PrettyTable()
    table.field_names = ["Row Number", "Rule Name", "Source", "Destination", "Service"]
    table.max_width = 50  # Limit column width for better readability
    
    for result in results:
        table.add_row([
            result["Row Number"],
            result["Rule Name"],
            result["Source"][:50] + ('...' if len(result["Source"]) > 50 else ''),
            result["Destination"][:50] + ('...' if len(result["Destination"]) > 50 else ''),
            result["Service"][:50] + ('...' if len(result["Service"]) > 50 else '')
        ])
    
    print("\nMatching Rules (Source: Any, Destination: Any, Service: Any):\n")
    print(table)
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'output_Source-Any--Destination-Any--Services-Any.xlsx'
results_df = pd.DataFrame(results)
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
