import pandas as pd
import ipaddress
import re
from tabulate import tabulate
from multiprocessing import Pool, cpu_count

def is_public_ip(ip_str):
    """Check if an IP address or subnet is public."""
    try:
        network = ipaddress.ip_network(ip_str, strict=False)
        # Check if it's not private, loopback, link-local, or multicast
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
    """Extract valid IP addresses and subnets from a given text string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)

def process_rule(row, cde_data):
    """Process a single firewall rule for analysis."""
    excel_row = row['Excel Row']
    source = row['Source']
    destination = row['Destination']
    service = row.get('Service', 'N/A')

    cde_ranges, cde_strings = cde_data

    source_items = extract_ips(source)
    destination_items = extract_ips(destination)

    # Get public IPs
    source_public_ips = [(ip, is_public_ip(ip)) for ip in source_items]
    dest_public_ips = [(ip, is_public_ip(ip)) for ip in destination_items]
    
    source_public = any(is_public for _, is_public in source_public_ips)
    dest_public = any(is_public for _, is_public in dest_public_ips)

    source_cde_matches = []
    dest_cde_matches = []

    for item in source_items:
        source_cde_matches.extend(map_ip_to_ranges(item, cde_ranges, cde_strings))

    for item in destination_items:
        dest_cde_matches.extend(map_ip_to_ranges(item, cde_ranges, cde_strings))

    findings = []

    if source_public and dest_cde_matches:
        # Get all public IPs found in source
        public_ips = [ip for ip, is_public in source_public_ips if is_public]
        findings.append({
            "Finding_Type": "Public Source to CDE Destination",
            "Excel Row": excel_row,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Public_IP": '\n'.join(public_ips),
            "CDE_Range": '\n'.join(dest_cde_matches)
        })
    if source_cde_matches and dest_public:
        # Get all public IPs found in destination
        public_ips = [ip for ip, is_public in dest_public_ips if is_public]
        findings.append({
            "Finding_Type": "CDE Source to Public Destination",
            "Excel Row": excel_row,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Public_IP": '\n'.join(public_ips),
            "CDE_Range": '\n'.join(source_cde_matches)
        })

    return findings

def analyze_rules_parallel(rules_df, cde_data):
    """Analyze rules using parallel processing."""
    rules_df['Excel Row'] = rules_df.index + 2
    rules = rules_df.to_dict(orient='records')

    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_rule,
            [(rule, cde_data) for rule in rules]
        )

    findings = [finding for result in results for finding in result]
    return findings

def display_and_save_results(rules_df, findings):
    """Display and save results."""
    print("\nAll Rules:")
    print(tabulate(rules_df, headers='keys', tablefmt='fancy_grid', showindex=False))
    rules_df.to_excel("all_rules.xlsx", index=False)
    print("All rules saved to 'all_rules.xlsx'.")

    print("\nFindings:")
    findings_df = pd.DataFrame(findings)
    if not findings_df.empty:
        # Sort by Finding_Type
        findings_df = findings_df.sort_values('Finding_Type')
        
        column_order = [
            "Finding_Type",
            "Excel Row",
            "Source",
            "Destination",
            "Service",
            "Public_IP",
            "CDE_Range"
        ]
        findings_df = findings_df[column_order]
        
        # Rename columns for better clarity
        findings_df = findings_df.rename(columns={
            "Finding_Type": "Finding Type",
            "Excel Row": "Excel Row",
            "Public_IP": "Public IP/Subnet",
            "CDE_Range": "CDE Range"
        })
        
        print(tabulate(findings_df, headers='keys', tablefmt='fancy_grid', showindex=False))
        findings_df.to_excel("findings2.xlsx", index=False)
        print("Findings saved to 'findings2.xlsx'.")
    else:
        print("  No findings reported.")

def main(excel_file, cde_file):
    """Main function to load data and analyze rules."""
    try:
        print("Loading CDE network ranges...")
        cde_data = load_ip_ranges(cde_file)
        print(f"Loaded {len(cde_data[0])} CDE ranges")

        print("Loading firewall rules...")
        rules_df = pd.read_excel(excel_file, header=0).dropna(how='all').drop_duplicates()
        print(f"Total rules loaded: {rules_df.shape[0]}")

        print("Analyzing rules...")
        findings = analyze_rules_parallel(rules_df, cde_data)
        display_and_save_results(rules_df, findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    excel_file = input("Enter the Excel file name (with .xlsx): ")
    cde_file = 'cde.txt'
    main(excel_file, cde_file)
