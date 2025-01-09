import pandas as pd
from prettytable import PrettyTable
import re

def normalize_value(value):
    return str(value).lower().strip()

def is_any_value(item):
    item = normalize_value(item)
    patterns = [
        '^any$',  # Matches standalone "any"
        r'^\[[\w\s-]+\]\s*any$'  # Matches [anything] any
    ]
    return any(re.match(pattern, item, re.IGNORECASE) for pattern in patterns)

def is_all_any(value):
    if pd.isna(value) or str(value).strip() == '':
        return True
    value_str = str(value).replace(';', '\n')
    lines = [line.strip() for line in value_str.split('\n') if line.strip()]
    return not lines or all(is_any_value(line) for line in lines)

def has_specific_value(value):
    if pd.isna(value) or str(value).strip() == '':
        return False
    value_str = str(value).replace(';', '\n')
    lines = [line.strip() for line in value_str.split('\n') if line.strip()]
    return any(not is_any_value(line) for line in lines)

try:
    df = pd.read_excel('modified_firewall_updated.xlsx')
except FileNotFoundError:
    print("Error: File not found.")
    exit()
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

results = []
for index, row in df.iterrows():
    source = str(row['Source'])
    destination = str(row['Destination'])
    service = str(row['Service'])
    
    if has_specific_value(source) and is_all_any(destination):
        results.append({
            "Row Number": index + 2,
            "Rule Name": row.get('Rule', 'N/A'),
            "Source": source,
            "Destination": destination,
            "Service": service,
        })

if results:
    table = PrettyTable()
    table.field_names = ["Row Number", "Rule Name", "Source", "Destination", "Service"]
    table.max_width = 50
    
    for result in results:
        table.add_row([
            result["Row Number"],
            result["Rule Name"],
            result["Source"][:50] + ('...' if len(result["Source"]) > 50 else ''),
            result["Destination"][:50] + ('...' if len(result["Destination"]) > 50 else ''),
            result["Service"][:50] + ('...' if len(result["Service"]) > 50 else '')
        ])
    
    print("\nMatching Rules (Source: Specific, Destination: Any, Service: Any/Specific):\n")
    print(table)
else:
    print("No matching rules found.")

output_file = 'Source-Specific--Destination-Any--Services-Any-Specific.xlsx'
pd.DataFrame(results).to_excel(output_file, index=False)
print(f"\nResults saved to {output_file}")
