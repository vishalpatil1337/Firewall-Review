import pandas as pd
from tabulate import tabulate  # Ensure you install this library using `pip install tabulate`
import os

# Adjust terminal width (Optional for better display)
os.system('mode con: cols=150')  # Sets CMD window to 150 columns wide

# Load the Excel file
file_path = 'modified_firewall_updated.xlsx'
df = pd.read_excel(file_path)

# Print the column names to understand the structure (optional)
print("Column names in the DataFrame:")
print(df.columns)

# Prepare a list to hold the results
results = []

# Check each rule in the DataFrame
for index, row in df.iterrows():
    # Normalize values to lowercase for case-insensitive comparison
    source = str(row['Source']).strip().lower()
    destination = str(row['Destination']).strip().lower()
    service = str(row['Service']).strip().lower()

    # Check if source and destination are specific (not 'any') and service is 'any'
    if source != 'any' and destination != 'any' and service == 'any':
        # Add 2 to index to account for the header row and 1-based index
        results.append({
            "Row Number": index + 2,
            "Rule Name": row.get('Rule', 'N/A'),
            "Source": row['Source'],
            "Destination": row['Destination'],
            "Service": row['Service'],
        })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)

# Print results to the console with formatting
if not results_df.empty:
    print("\nMatching Rules (Source: Specific, Destination: Specific, Service: any):\n")
    print(tabulate(results_df, headers='keys', tablefmt='grid', showindex=False))
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-Specific--Destination-Specific--Services-Any.xlsx'
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
