"""
Firewall Rule Checker - External to Internal Analysis Tool
Analyzes firewall rules for communications between external and internal networks.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import ipaddress
import re
from tabulate import tabulate
from multiprocessing import Pool, cpu_count

class IPAnalyzer:
    """Handles IP address analysis and validation."""
    
    # RFC 1918 Private Network Ranges
    PRIVATE_NETWORKS = [
        ipaddress.ip_network('10.0.0.0/8'),      # 10.0.0.0 - 10.255.255.255
        ipaddress.ip_network('172.16.0.0/12'),   # 172.16.0.0 - 172.31.255.255
        ipaddress.ip_network('192.168.0.0/16'),  # 192.168.0.0 - 192.168.255.255
    ]
    
    def __init__(self):
        self.ip_cache = {}  # Cache for IP classification results

    def is_private_ip(self, ip_str: str) -> bool:
        """
        Check if an IP address or subnet is private according to RFC 1918.
        Also handles other special-use IPv4 addresses.
        """
        try:
            # Check cache first
            if ip_str in self.ip_cache:
                return self.ip_cache[ip_str]

            # Handle both individual IPs and subnets
            ip_obj = ipaddress.ip_network(ip_str, strict=False)
            
            # Check if it's a special use or private address
            is_private = (
                any(ip_obj.overlaps(network) for network in self.PRIVATE_NETWORKS) or
                ip_obj.is_private or
                ip_obj.is_loopback or
                ip_obj.is_link_local or
                ip_obj.is_multicast or
                ip_obj.is_reserved or
                ip_obj.is_unspecified
            )

            # Cache the result
            self.ip_cache[ip_str] = is_private
            return is_private

        except ValueError:
            return False

    def extract_ips(self, text: str) -> list:
        """Extract IP addresses and subnets from text."""
        ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)'
        return re.findall(ip_pattern, str(text))

def process_rule(row, ip_analyzer):
    """Process a single firewall rule."""
    excel_row = row['Excel Row']
    rule_number = row.get('Rule ID', 'N/A')
    source = str(row['Source'])
    destination = str(row['Destination'])
    service = str(row.get('Service', 'N/A'))

    findings = []

    # Extract IPs
    source_ips = ip_analyzer.extract_ips(source)
    dest_ips = ip_analyzer.extract_ips(destination)

    # Analyze source IPs
    source_public = []
    source_private = []
    for ip in source_ips:
        if ip_analyzer.is_private_ip(ip):
            source_private.append(ip)
        else:
            source_public.append(ip)

    # Analyze destination IPs
    dest_public = []
    dest_private = []
    for ip in dest_ips:
        if ip_analyzer.is_private_ip(ip):
            dest_private.append(ip)
        else:
            dest_public.append(ip)

    # Check for public to private communication
    if source_public and dest_private:
        findings.append({
            "Type": "Public Source to Private Destination",
            "Excel Row": excel_row,
            "Rule Number": rule_number,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Public IPs": '\n'.join(source_public),
            "Private IPs": '\n'.join(dest_private)
        })

    # Check for private to public communication
    if source_private and dest_public:
        findings.append({
            "Type": "Private Source to Public Destination",
            "Excel Row": excel_row,
            "Rule Number": rule_number,
            "Source": source,
            "Destination": destination,
            "Service": service,
            "Private IPs": '\n'.join(source_private),
            "Public IPs": '\n'.join(dest_public)
        })

    return findings

def analyze_rules_parallel(rules_df):
    """Analyze rules using parallel processing."""
    # Add Excel row number
    rules_df['Excel Row'] = rules_df.index + 2
    rules = rules_df.to_dict(orient='records')
    
    # Create IP analyzer instance
    ip_analyzer = IPAnalyzer()

    # Process rules in parallel
    with Pool(cpu_count()) as pool:
        results = pool.starmap(
            process_rule,
            [(rule, ip_analyzer) for rule in rules]
        )

    # Flatten results
    findings = [finding for result in results for finding in result]
    return findings

def display_and_save_results(rules_df, findings):
    """Display and save analysis results."""
    # Save all rules for reference
    rules_df.to_excel("all_rules.xlsx", index=False)
    print("All rules saved to 'all_rules.xlsx'.")

    # Process findings
    if findings:
        findings_df = pd.DataFrame(findings)
        
        # Sort findings by type and row number
        findings_df = findings_df.sort_values(['Type', 'Excel Row'])
        
        # Display findings
        print("\nFindings:")
        print(tabulate(findings_df, headers='keys', tablefmt='grid', showindex=False))
        
        # Save findings
        findings_df.to_excel("output_external_internal.xlsx", index=False)
        print("Findings saved to 'output_external_internal.xlsx'.")
        
        # Print summary statistics
        print("\nSummary by Rule Type:")
        for rule_type in findings_df['Type'].unique():
            type_findings = findings_df[findings_df['Type'] == rule_type]
            print(f"\n{rule_type}:")
            print(f"Total findings: {len(type_findings)}")
            print("Affected Rule Numbers:", ', '.join(map(str, type_findings['Rule Number'].unique())))
    else:
        print("\nNo findings reported.")

def main():
    """Main execution function."""
    try:
        excel_file = 'modified_firewall_updated.xlsx'

        print("Loading firewall rules...")
        rules_df = pd.read_excel(excel_file, header=0).dropna(how='all').drop_duplicates()
        print(f"Total rules loaded: {rules_df.shape[0]}")

        # Verify Rule ID column exists
        if 'Rule ID' not in rules_df.columns:
            print("Warning: 'Rule ID' column not found in Excel file. Using sequential numbers.")
            rules_df['Rule ID'] = range(1, len(rules_df) + 1)

        print("Analyzing rules...")
        findings = analyze_rules_parallel(rules_df)
        display_and_save_results(rules_df, findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check if required files exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
