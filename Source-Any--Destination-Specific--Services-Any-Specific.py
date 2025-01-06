import pandas as pd
from prettytable import PrettyTable  # Install with `pip install prettytable`

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

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    # Normalize values to lowercase for case-insensitive comparison
    source = str(row['Source']).strip().lower()
    destination = str(row['Destination']).strip().lower()
    service = str(row['Service']).strip().lower()

    # Check conditions for the rule
    if (source == 'any' or '[zone] any' in source) and destination != 'any':  # Destination must not be 'any'
        results.append({
            "Row Number": index + 2,
            "Rule Name": row.get('Rule', 'N/A'),
            "Source": 'Any',  # Report as 'Any' if it matches the condition
            "Destination": row['Destination'],
            "Service": row['Service'],
        })

# Print results to the console with formatting
if results:
    table = PrettyTable()
    table.field_names = ["Row Number", "Rule Name", "Source", "Destination", "Service"]
    for result in results:
        table.add_row([result["Row Number"], result["Rule Name"], result["Source"], result["Destination"], result["Service"]])
    print("\nMatching Rules (Source: Any, Destination: Specific, Service: Any/Specific):\n")
    print(table)
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-Any--Destination-Specific--Services-Any-Specific.xlsx'
results_df = pd.DataFrame(results)
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
