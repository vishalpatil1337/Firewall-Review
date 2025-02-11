"""
Firewall Rule Checker - CDE to External Analysis Tool
Analyzes firewall rules for communications between CDE and external networks.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import ipaddress
import re
from tabulate import tabulate
from multiprocessing import Pool, cpu_count

def is_public_ip(ip_str):
    """Check if an IP address or subnet is public."""
    try:
        network = ipaddress.ip_network(ip_str, strict=False)
        return not (
            network.is_private or
            network.is_loopback or
            network.is_link_local or
            network.is_multicast or
            network.is_reserved
        )
    except ValueError:
        return False

def load_ip_ranges(file_path):
    """Load IP ranges from a file and return as list of strings and network objects."""
    ranges = []
    range_strings = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            try:
                network = ipaddress.ip_network(line, strict=False)
                ranges.append(network)
                range_strings.append(line)
            except ValueError:
                continue
    return ranges, range_strings

def map_ip_to_ranges(ip_str, network_ranges, range_strings):
    """Maps an IP/subnet to its matching ranges."""
    matches = []
    try:
        ip_net = ipaddress.ip_network(ip_str, strict=False)
        if ip_str in range_strings:
            matches.append(f"{ip_str}")
        else:
            for network, range_str in zip(network_ranges, range_strings):
                if network.overlaps(ip_net):
                    matches.append(range_str)
        return matches
    except ValueError:
        return []

def extract_ips(text):
    """Extract valid IP addresses and subnets from text."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)

def process_rule(row, cde_data):
    """Process a single firewall rule."""
    excel_row = row['Excel Row']
    rule_number = row.get('Rule ID', 'N/A')
    source = row['Source']
    destination = row['Destination']
    service = row.get('Service', 'N/A')

    cde_ranges, cde_strings = cde_data

    # Extract and validate IPs
    source_ips = extract_ips(source)
    dest_ips = extract_ips(destination)

    # Get public IPs and CDE matches
    source_public_ips = [(ip, is_public_ip(ip)) for ip in source_ips]
    dest_public_ips = [(ip, is_public_ip(ip)) for ip in dest_ips]
    
    source_public = any(is_public for _, is_public in source_public_ips)
    dest_public = any(is_public for _, is_public in dest_public_ips)

    source_cde_matches = []
    dest_cde_matches = []

    for ip in source_ips:
        source_cde_matches.extend(map_ip_to_ranges(ip, cde_ranges, cde_strings))

    for ip in dest_ips:
        dest_cde_matches.extend(map_ip_to_ranges(ip, cde_ranges, cde_strings))

    findings = []

    # Check for public source to CDE destination
    if source_public and dest_cde_matches:
        public_ips = [ip for ip, is_public in source_public_ips if is_public]
        findings.append({
            "Type": "Public Source to CDE Destination",
            "Excel Row": excel_row,
            "Rule Number": rule_number,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Public_IP": '\n'.join(public_ips),
            "CDE_Range": '\n'.join(dest_cde_matches)
        })

    # Check for CDE source to public destination
    if source_cde_matches and dest_public:
        public_ips = [ip for ip, is_public in dest_public_ips if is_public]
        findings.append({
            "Type": "CDE Source to Public Destination",
            "Excel Row": excel_row,
            "Rule Number": rule_number,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Public_IP": '\n'.join(public_ips),
            "CDE_Range": '\n'.join(source_cde_matches)
        })

    return findings

def analyze_rules_parallel(rules_df, cde_data):
    """Analyze rules using parallel processing."""
    rules_df['Excel Row'] = rules_df.index + 2  # Add Excel row number
    rules = rules_df.to_dict(orient='records')

    # Process rules in parallel
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_rule,
            [(rule, cde_data) for rule in rules]
        )

    # Flatten results
    findings = [finding for result in results for finding in result]
    return findings

def display_and_save_results(rules_df, findings):
    """Display and save analysis results."""
    # Save all rules
    rules_df.to_excel("all_rules.xlsx", index=False)
    print("All rules saved to 'all_rules.xlsx'.")

    # Display and save findings
    print("\nFindings:")
    findings_df = pd.DataFrame(findings)
    if not findings_df.empty:
        # Sort by Finding_Type
        findings_df = findings_df.sort_values('Type')
        
        # Reorder columns
        column_order = [
            "Type",
            "Excel Row",
            "Rule Number",
            "Source",
            "Destination",
            "Service",
            "Public_IP",
            "CDE_Range"
        ]
        findings_df = findings_df[column_order]
        
        # Rename columns for better clarity
        findings_df = findings_df.rename(columns={
            "Public_IP": "Public IP/Subnet",
            "CDE_Range": "CDE Range"
        })
        
        print(tabulate(findings_df, headers='keys', tablefmt='grid', showindex=False))
        findings_df.to_excel("output_cde-external.xlsx", index=False)
        print("Findings saved to 'output_cde-external.xlsx'.")
        
        # Print summary with rule numbers
        print("\nSummary by Rule Type:")
        for rule_type in findings_df['Type'].unique():
            type_findings = findings_df[findings_df['Type'] == rule_type]
            print(f"\n{rule_type}:")
            print(f"Total findings: {len(type_findings)}")
            print("Affected Rule Numbers:", ', '.join(map(str, type_findings['Rule Number'].unique())))
    else:
        print("No findings reported.")

def main():
    """Main execution function."""
    try:
        excel_file = 'modified_firewall_updated.xlsx'
        cde_file = 'cde.txt'

        print("Loading CDE network ranges...")
        cde_data = load_ip_ranges(cde_file)
        print(f"Loaded {len(cde_data[0])} CDE ranges")

        print("Loading firewall rules...")
        rules_df = pd.read_excel(excel_file, header=0).dropna(how='all').drop_duplicates()
        print(f"Total rules loaded: {rules_df.shape[0]}")

        # Verify Rule ID column exists
        if 'Rule ID' not in rules_df.columns:
            print("Warning: 'Rule ID' column not found in Excel file. Using sequential numbers.")
            rules_df['Rule ID'] = range(1, len(rules_df) + 1)

        print("Analyzing rules...")
        findings = analyze_rules_parallel(rules_df, cde_data)
        display_and_save_results(rules_df, findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check if required files exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
