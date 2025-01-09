import pandas as pd
from prettytable import PrettyTable

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

def is_all_any(value):
    # Handle empty/NaN values
    if pd.isna(value) or str(value).strip() == '':
        return True
        
    # Split the value into lines (handling both newline characters and semicolons)
    lines = str(value).replace(';', '\n').split('\n')
    
    # Clean and check each line
    for line in lines:
        line = line.strip()
        if line and not (line.lower() == 'any' or (line.lower().startswith('[') and line.lower().endswith(' any'))):
            return False
    return True

def is_specific(value):
    return not is_all_any(value)

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    source = str(row['Source'])
    destination = str(row['Destination'])
    service = str(row['Service'])
    
    # Check conditions: Source must be 'any', Destination must be specific
    if is_all_any(source) and is_specific(destination):
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
    print("\nMatching Rules (Source: Any, Destination: Specific, Service: Any/Specific):\n")
    print(table)
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-Any--Destination-Specific--Services-Any-Specific.xlsx'
results_df = pd.DataFrame(results)
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
