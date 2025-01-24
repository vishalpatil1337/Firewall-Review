import pandas as pd
import ipaddress
import re
from tabulate import tabulate
from multiprocessing import Pool, cpu_count


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
    """
    Maps an IP/subnet to its matching ranges, but only if the exact range exists in the file.
    """
    matches = []
    try:
        ip_net = ipaddress.ip_network(ip_str, strict=False)
        # Only include match if the exact IP/subnet is in the file
        if ip_str in range_strings:
            matches.append(f"{ip_str}")
        else:
            # Check if this IP/subnet is within any of the defined ranges
            for network, range_str in zip(network_ranges, range_strings):
                if network.overlaps(ip_net):
                    matches.append(f"{ip_str} matched with {range_str}")
        return matches
    except ValueError:
        return []


def extract_ips(text):
    """Extract valid IP addresses and subnets from a given text string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)


def process_rule(row, cde_data, oos_data):
    """Process a single firewall rule for analysis."""
    excel_row = row['Excel Row']
    source = row['Source']
    destination = row['Destination']
    service = row.get('Service', 'N/A')

    cde_ranges, cde_strings = cde_data
    oos_ranges, oos_strings = oos_data

    source_items = extract_ips(source)
    destination_items = extract_ips(destination)

    # Get matching information for each IP/subnet
    source_oos_matches = []
    source_cde_matches = []
    dest_oos_matches = []
    dest_cde_matches = []

    for item in source_items:
        source_oos_matches.extend(map_ip_to_ranges(item, oos_ranges, oos_strings))
        source_cde_matches.extend(map_ip_to_ranges(item, cde_ranges, cde_strings))

    for item in destination_items:
        dest_oos_matches.extend(map_ip_to_ranges(item, oos_ranges, oos_strings))
        dest_cde_matches.extend(map_ip_to_ranges(item, cde_ranges, cde_strings))

    findings = []

    if source_oos_matches and dest_cde_matches:
        findings.append({
            "Type": "Out of Scope Source to CDE Destination",
            "Excel Row": excel_row,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Matching_Source_Ranges": '\n'.join(source_oos_matches),
            "Matching_Destination_Ranges": '\n'.join(dest_cde_matches)
        })
    if source_cde_matches and dest_oos_matches:
        findings.append({
            "Type": "CDE Source to Out of Scope Destination",
            "Excel Row": excel_row,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Matching_Source_Ranges": '\n'.join(source_cde_matches),
            "Matching_Destination_Ranges": '\n'.join(dest_oos_matches)
        })

    return findings


def analyze_rules_parallel(rules_df, cde_data, oos_data):
    """Analyze rules using parallel processing."""
    rules_df['Excel Row'] = rules_df.index + 2  # Add Excel row number

    # Convert DataFrame rows to dictionaries for processing
    rules = rules_df.to_dict(orient='records')

    # Process rules in parallel
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_rule,
            [(rule, cde_data, oos_data) for rule in rules]
        )

    # Flatten results
    findings = [finding for result in results for finding in result]

    return findings


def display_and_save_results(rules_df, findings):
    """Display and save results."""
    # Display all rules
    print("\nAll Rules:")
    print(tabulate(rules_df, headers='keys', tablefmt='fancy_grid', showindex=False))
    rules_df.to_excel("all_rules.xlsx", index=False)
    print("All rules saved to 'all_rules.xlsx'.")

    # Display findings
    print("\nFindings:")
    findings_df = pd.DataFrame(findings)
    if not findings_df.empty:
        # Reorder columns to put matching ranges in columns I and J
        column_order = [
            "Type", "Excel Row", "Source", "Destination", "Service",
            "Matching_Source_Ranges", "Matching_Destination_Ranges"
        ]
        findings_df = findings_df[column_order]
        
        print(tabulate(findings_df, headers='keys', tablefmt='fancy_grid', showindex=False))
        findings_df.to_excel("output_cde-oos-findings.xlsx", index=False)
        print("Findings saved to 'output_cde-oos-findings.xlsx'.")
    else:
        print("  No findings reported.")


def main(excel_file, cde_file, oos_file):
    """Main function to load data and analyze rules."""
    try:
        print("Loading network ranges...")
        cde_data = load_ip_ranges(cde_file)
        oos_data = load_ip_ranges(oos_file)
        print(f"Loaded {len(cde_data[0])} CDE ranges and {len(oos_data[0])} OOS ranges")

        print("Loading firewall rules...")
        rules_df = pd.read_excel(excel_file, header=0).dropna(how='all').drop_duplicates()
        print(f"Total rules loaded: {rules_df.shape[0]}")

        print("Analyzing rules...")
        findings = analyze_rules_parallel(rules_df, cde_data, oos_data)
        display_and_save_results(rules_df, findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    excel_file = input("Enter the Excel file name (with .xlsx): ")
    cde_file = 'cde.txt'
    oos_file = 'oos.txt'
    main(excel_file, cde_file, oos_file)
