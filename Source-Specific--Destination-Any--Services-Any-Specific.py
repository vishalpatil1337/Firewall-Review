import pandas as pd
from tabulate import tabulate

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
    source = str(row['Source']).strip().lower()  # Get the source from the DataFrame
    destination = str(row['Destination']).strip().lower()  # Get the destination from the DataFrame
    service = str(row['Service']).strip().lower()  # Get the service from the DataFrame

    # Check if source is specific, destination is any, and service is any/specific
    if source != 'any' and destination == 'any':
        # Add 2 to index to account for the header row and 1-based index
        results.append({
            "Row Number": index + 2,  # Adjust for 1-based index and header row
            "Rule Name": row.get('Rule', 'N/A'),  # Adjust if there's a Rule Name column
            "Source": source,
            "Destination": destination,
            "Service": service,
        })

# Create a DataFrame for the results
results_df = pd.DataFrame(results)

# Print results to the console with formatting
if not results_df.empty:
    print("\nMatching Rules (Source: Specific, Destination: any, Service: any/specific):")
    print(tabulate(results_df, headers='keys', tablefmt='pretty', showindex=False))
else:
    print("No matching rules found.")

# Save results to a new Excel file
output_file_path = 'Source-Specific--Destination-Any--Services-Any-Specific.xlsx'
results_df.to_excel(output_file_path, index=False)
print(f"\nResults saved to {output_file_path}")
