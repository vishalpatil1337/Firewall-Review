import pandas as pd
import ipaddress
import re
from tabulate import tabulate


def load_ip_ranges(file_path):
    """Load IP ranges from a file and return them as ip_network objects."""
    ranges = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            try:
                network = ipaddress.ip_network(line, strict=False)
                ranges.append(network)
            except ValueError:
                continue  # Skip invalid entries
    return ranges


def ip_or_subnet_in_ranges(ip_or_subnet, ranges):
    """Check if an IP or subnet is in the given ranges."""
    try:
        ip_network = ipaddress.ip_network(ip_or_subnet, strict=False)
        return any(ip_network.subnet_of(range) or ip_network == range for range in ranges)
    except ValueError:
        ip = ipaddress.ip_address(ip_or_subnet)
        return any(ip in range for range in ranges)


def extract_ips(text):
    """Extract valid IP addresses and subnets from a given text string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)


def analyze_rules(rules_df, cde_ranges, oos_ranges):
    """Analyze rules for specific conditions."""
    all_rules = []
    findings = []

    for index, row in rules_df.iterrows():
        source = row['Source']
        destination = row['Destination']
        service = row.get('Service', 'N/A')

        excel_row = index + 2

        source_items = extract_ips(source)
        destination_items = extract_ips(destination)

        # Check for matches in CDE and OOS ranges
        oos_source = any(ip_or_subnet_in_ranges(item, oos_ranges) for item in source_items)
        cde_destination = any(ip_or_subnet_in_ranges(item, cde_ranges) for item in destination_items)

        cde_source = any(ip_or_subnet_in_ranges(item, cde_ranges) for item in source_items)
        oos_destination = any(ip_or_subnet_in_ranges(item, oos_ranges) for item in destination_items)

        # Debugging: Print which IPs are being matched
        print(f"Row {excel_row}: Source IPs: {source_items}, Destination IPs: {destination_items}")
        print(f"  OOS Source Match: {oos_source}, CDE Destination Match: {cde_destination}")
        print(f"  CDE Source Match: {cde_source}, OOS Destination Match: {oos_destination}")

        # Save all rules
        all_rules.append({
            "Excel Row": excel_row,
            "Source": source,
            "Destination": destination,
            "Service": service
        })

        # Save findings for each condition
        if oos_source and cde_destination:
            findings.append({
                "Type": "Out of Scope Source to CDE Destination",
                "Excel Row": excel_row,
                "Source": source,
                "Destination": destination,
                "Service": service
            })
        if cde_source and oos_destination:
            findings.append({
                "Type": "CDE Source to Out of Scope Destination",
                "Excel Row": excel_row,
                "Source": source,
                "Destination": destination,
                "Service": service
            })
        if cde_destination and oos_source:
            findings.append({
                "Type": "CDE Destination to Out of Scope Source",
                "Excel Row": excel_row,
                "Source": source,
                "Destination": destination,
                "Service": service
            })
        if oos_destination and cde_source:
            findings.append({
                "Type": "Out of Scope Destination to CDE Source",
                "Excel Row": excel_row,
                "Source": source,
                "Destination": destination,
                "Service": service
            })

    return all_rules, findings


def display_and_save_results(all_rules, findings):
    """Display and save results."""
    all_rules_df = pd.DataFrame(all_rules)
    findings_df = pd.DataFrame(findings)

    # Display all rules
    print("\nAll Rules:")
    print(tabulate(all_rules_df, headers='keys', tablefmt='fancy_grid', showindex=False))
    all_rules_df.to_excel("all_rules.xlsx", index=False)
    print("All rules saved to 'all_rules.xlsx'.")

    # Display findings
    print("\nFindings:")
    if not findings_df.empty:
        print(tabulate(findings_df, headers='keys', tablefmt='fancy_grid', showindex=False))
        findings_df.to_excel("findings.xlsx", index=False)
        print("Findings saved to 'findings.xlsx'.")
    else:
        print("  No findings reported.")


def main(excel_file, cde_file, oos_file):
    """Main function to load data and analyze rules."""
    try:
        cde_ranges = load_ip_ranges(cde_file)
        oos_ranges = load_ip_ranges(oos_file)

        rules_df = pd.read_excel(excel_file, header=0)
        rules_df = rules_df.dropna(how='all')
        rules_df = rules_df.drop_duplicates()

        print(f"Total rules loaded: {rules_df.shape[0]}")

        all_rules, findings = analyze_rules(rules_df, cde_ranges, oos_ranges)
        display_and_save_results(all_rules, findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    excel_file = input("Enter the Excel file name (with .xlsx): ")
    cde_file = 'cde.txt'
    oos_file = 'oos.txt'
    main(excel_file, cde_file, oos_file)
