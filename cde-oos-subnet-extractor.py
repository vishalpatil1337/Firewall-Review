import pandas as pd
import ipaddress
import re
from tabulate import tabulate

def is_external(ip):
    """Check if an IP is external (public)."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        # Check if the IP is in any of the private ranges
        return not (ip_obj in ipaddress.ip_network("10.0.0.0/8") or
                    ip_obj in ipaddress.ip_network("172.16.0.0/12") or
                    ip_obj in ipaddress.ip_network("192.168.0.0/16"))
    except ValueError:
        return False  # Invalid IP

def extract_ips(text):
    """Extract valid IP addresses from a given text string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)

def analyze_rules(rules_df):
    """Analyze rules for external IPs in Source and Destination."""
    findings = []

    for index, row in rules_df.iterrows():
        source = row['Source']
        destination = row['Destination']
        service = row.get('Service', 'N/A')
        excel_row = index + 2  # Adjust for Excel numbering (header row is row 1)

        # Check if both source and destination are external
        if is_external(source) and is_external(destination):
            findings.append({
                "Excel Row": excel_row,
                "Source": source,
                "Destination": destination,
                "Service": service
            })

    return findings

def display_and_save_results(findings):
    """Display and save results."""
    findings_df = pd.DataFrame(findings)

    print("\nFindings:")
    if not findings_df.empty:
        print(tabulate(findings_df, headers='keys', tablefmt='fancy_grid', showindex=False))
        findings_df.to_csv("findings.csv", index=False)
        print("Findings saved to 'findings.csv'.")
    else:
        print("  No findings reported.")

def main(excel_file):
    """Main function to load data and analyze rules."""
    try:
        # Read only columns C and D (Source and Destination)
        rules_df = pd.read_excel(excel_file, header=0, usecols="C,D,E")  
        rules_df.columns = ['Source', 'Destination', 'Service']  # Rename columns for easier access
        rules_df = rules_df.dropna(how='all')  # Drop rows where all elements are NaN
        rules_df = rules_df.drop_duplicates()  # Drop duplicate rows

        print(f"Total rules loaded: {rules_df.shape[0]}")

        findings = analyze_rules(rules_df)
        display_and_save_results(findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Prompt the user for the Excel file name
    excel_file = input("Enter the Excel file name (with .xlsx): ")
    
    # Call the main function with the specified Excel file
    main(excel_file)
