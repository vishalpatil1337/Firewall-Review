import pandas as pd
import ipaddress
import re

def is_private(ip):
    """Check if an IP address is private."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        # Fix for 172.168.x.x being incorrectly flagged as private
        if ip_obj in ipaddress.ip_network('10.0.0.0/8') or ip_obj in ipaddress.ip_network('172.16.0.0/12') or ip_obj in ipaddress.ip_network('192.168.0.0/16'):
            return True
        return False
    except ValueError:
        return False  # Invalid IP

def extract_ips(ip_string):
    """Extract valid IPs and ranges from a string."""
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?:-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?'
    matches = re.findall(ip_pattern, ip_string)
    
    extracted_ips = []
    for match in matches:
        start_ip = match[0]
        end_ip = match[1] if match[1] else start_ip  # If no end IP, use start IP
        
        # If range is provided, generate all IPs in the range
        if start_ip != end_ip:
            start_ip_obj = ipaddress.ip_address(start_ip)
            end_ip_obj = ipaddress.ip_address(end_ip)
            for ip in range(int(start_ip_obj), int(end_ip_obj) + 1):
                extracted_ips.append(str(ipaddress.ip_address(ip)))
        else:
            extracted_ips.append(start_ip)
    
    return extracted_ips

def find_public_ip(ip_list):
    """Find a public IP from a list of IPs."""
    for ip in ip_list:
        if not is_private(ip):
            return ip  # Return the first public IP found
    return None  # Return None if no public IP is found

def analyze_rules(rules_df):
    """Analyze rules for public/private IPs and find a public IP for each rule."""
    findings = []

    for index, row in rules_df.iterrows():
        source = row['Source']
        destination = row['Destination']
        services = row['Services']  # Assuming 'Services' column exists in the input file
        
        # Extract IPs from source and destination
        source_ips = extract_ips(source)
        destination_ips = extract_ips(destination)

        # Check if source is public and destination is private
        if any(not is_private(ip) for ip in source_ips) and any(is_private(ip) for ip in destination_ips):
            public_ip = find_public_ip(source_ips)
            findings.append({
                "Rule Type": "Public Source to Private Destination",
                "Row Number": index + 2,  # Corrected for Excel's 1-based index
                "Source": source,
                "Destination": destination,
                "Services": services,
                "Public IP": public_ip
            })

        # Check if source is private and destination is public
        if any(is_private(ip) for ip in source_ips) and any(not is_private(ip) for ip in destination_ips):
            public_ip = find_public_ip(destination_ips)
            findings.append({
                "Rule Type": "Private Source to Public Destination",
                "Row Number": index + 2,  # Corrected for Excel's 1-based index
                "Source": source,
                "Destination": destination,
                "Services": services,
                "Public IP": public_ip
            })

    return findings

def save_results(findings):
    """Save results to an Excel file."""
    findings_df = pd.DataFrame(findings)
    findings_df.to_excel("firewall_analysis_results.xlsx", index=False)
    print("Findings saved to 'firewall_analysis_results.xlsx'.")

def main(excel_file):
    """Main function to load data and analyze rules."""
    try:
        # Read the Excel file
        rules_df = pd.read_excel(excel_file, usecols="C,D,E")  # Read Source, Destination, and Services columns
        rules_df.columns = ['Source', 'Destination', 'Services']  # Rename columns for easier access

        print(f"Total rules loaded: {rules_df.shape[0]}")

        findings = analyze_rules(rules_df)

        # Display findings
        if findings:
            print("\nFindings:")
            for finding in findings:
                print(f"{finding['Rule Type']}: Row {finding['Row Number']}, Source: {finding['Source']}, Destination: {finding['Destination']}, Services: {finding['Services']}, Public IP: {finding['Public IP']}")
        else:
            print("No findings reported.")

        # Save results to Excel
        save_results(findings)

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Prompt the user for the Excel file name
    excel_file = input("Enter the Excel file name (with .xlsx): ")
    
    # Call the main function with the specified Excel file
    main(excel_file)
