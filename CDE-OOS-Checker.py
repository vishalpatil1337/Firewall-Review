import pandas as pd
import ipaddress
import re
from tabulate import tabulate
from multiprocessing import Pool, cpu_count


def load_ip_ranges(file_path):
    """Load IP ranges from a file and return precomputed sets for faster lookup."""
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


def precompute_ranges(ranges):
    """Precompute IP addresses in ranges for faster lookup."""
    return {str(ip) for r in ranges for ip in r.hosts()}


def extract_ips(text):
    """Extract valid IP addresses and subnets from a given text string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
    return re.findall(ip_pattern, text)


def process_rule(row, cde_precomputed, oos_precomputed):
    """Process a single firewall rule for analysis."""
    excel_row = row['Excel Row']
    source = row['Source']
    destination = row['Destination']
    service = row.get('Service', 'N/A')

    source_items = extract_ips(source)
    destination_items = extract_ips(destination)

    # Check for matches in CDE and OOS ranges
    oos_source = any(item in oos_precomputed for item in source_items)
    cde_destination = any(item in cde_precomputed for item in destination_items)

    cde_source = any(item in cde_precomputed for item in source_items)
    oos_destination = any(item in oos_precomputed for item in destination_items)

    findings = []

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

    return findings


def analyze_rules_parallel(rules_df, cde_ranges, oos_ranges):
    """Analyze rules using parallel processing."""
    cde_precomputed = precompute_ranges(cde_ranges)
    oos_precomputed = precompute_ranges(oos_ranges)

    rules_df['Excel Row'] = rules_df.index + 2  # Add Excel row number

    # Convert DataFrame rows to dictionaries for processing
    rules = rules_df.to_dict(orient='records')

    # Process rules in parallel
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_rule,
            [(rule, cde_precomputed, oos_precomputed) for rule in rules]
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

        rules_df = pd.read_excel(excel_file, header=0).dropna(how='all').drop_duplicates()
        print(f"Total rules loaded: {rules_df.shape[0]}")

        findings = analyze_rules_parallel(rules_df, cde_ranges, oos_ranges)
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
