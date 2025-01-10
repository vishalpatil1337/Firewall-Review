import pandas as pd
import ipaddress
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'firewall_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class FirewallAnalyzer:
    def __init__(self):
        # Define private networks
        self.private_networks = [
            ipaddress.ip_network('10.0.0.0/8'),
            ipaddress.ip_network('172.16.0.0/12'),
            ipaddress.ip_network('192.168.0.0/16')
        ]
        # Updated pattern to better handle Group tags
        self.ip_pattern = re.compile(r'\[Host\]\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

    def is_private(self, ip: str) -> bool:
        """Check if an IP address is private."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in network for network in self.private_networks)
        except ValueError:
            logging.warning(f"Invalid IP address: {ip}")
            return False

    def get_subnet_info(self, ip: str) -> str:
        """Get subnet information for an IP address."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            ip_parts = str(ip_obj).split('.')
            
            if ip_parts[0] == '10':
                return f'10.0.0.0/8 Network (First Octet: {ip_parts[0]})'
            elif ip_parts[0] == '172' and 16 <= int(ip_parts[1]) <= 31:
                return f'172.16.0.0/12 Network (First Two Octets: {ip_parts[0]}.{ip_parts[1]})'
            elif ip_parts[0] == '192' and ip_parts[1] == '168':
                return f'192.168.0.0/16 Network (First Three Octets: {ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]})'
            return 'Public Internet'
        except ValueError:
            return 'Invalid IP'

    def extract_ips(self, text: str) -> List[str]:
        """Extract IP addresses from text."""
        if not isinstance(text, str):
            return []
        return self.ip_pattern.findall(text)

    def analyze_rule(self, source: str, destination: str, services: str) -> List[Dict]:
        """Analyze a single rule and return all matching patterns."""
        findings = []
        source_ips = self.extract_ips(source)
        dest_ips = self.extract_ips(destination)

        if not source_ips or not dest_ips:
            return findings

        for src_ip in source_ips:
            src_is_private = self.is_private(src_ip)
            src_subnet = self.get_subnet_info(src_ip)

            for dst_ip in dest_ips:
                dst_is_private = self.is_private(dst_ip)
                dst_subnet = self.get_subnet_info(dst_ip)

                # Check for private to public pattern
                if src_is_private and not dst_is_private:
                    findings.append({
                        'pattern': 'Private to Public',
                        'source_ip': src_ip,
                        'source_subnet': src_subnet,
                        'destination_ip': dst_ip,
                        'destination_subnet': dst_subnet,
                        'services': services
                    })
                # Check for public to private pattern
                elif not src_is_private and dst_is_private:
                    findings.append({
                        'pattern': 'Public to Private',
                        'source_ip': src_ip,
                        'source_subnet': src_subnet,
                        'destination_ip': dst_ip,
                        'destination_subnet': dst_subnet,
                        'services': services
                    })

        return findings

def analyze_firewall_rules(filename: str) -> None:
    """Main function to analyze firewall rules."""
    try:
        # Load Excel file
        df = pd.read_excel(filename, usecols="C,D,E", names=['Source', 'Destination', 'Services'])
        logging.info(f"Loaded {len(df)} rules from {filename}")

        analyzer = FirewallAnalyzer()
        all_findings = []

        # Analyze each rule
        for index, row in df.iterrows():
            try:
                findings = analyzer.analyze_rule(
                    str(row['Source']), 
                    str(row['Destination']), 
                    str(row['Services'])
                )
                
                for finding in findings:
                    all_findings.append({
                        'Row': index + 2,
                        'Pattern': finding['pattern'],
                        'Source IP': finding['source_ip'],
                        'Source Network': finding['source_subnet'],
                        'Destination IP': finding['destination_ip'],
                        'Destination Network': finding['destination_subnet'],
                        'Services': finding['services'],
                        'Original Source': row['Source'],
                        'Original Destination': row['Destination']
                    })
                    
                    logging.info(
                        f"Row {index + 2}: Found {finding['pattern']} pattern\n"
                        f"Source: {finding['source_ip']} ({finding['source_subnet']})\n"
                        f"Destination: {finding['destination_ip']} ({finding['destination_subnet']})"
                    )
                    
            except Exception as e:
                logging.error(f"Error analyzing row {index + 2}: {e}")
                continue

        # Save results
        if all_findings:
            output_file = f'firewall_analysis_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            pd.DataFrame(all_findings).to_excel(output_file, index=False)
            logging.info(f"Saved {len(all_findings)} findings to {output_file}")

            # Print summary
            print("\nAnalysis Summary:")
            print(f"Total rules analyzed: {len(df)}")
            print(f"Rules with findings: {len(all_findings)}")
            print("\nDetailed Findings:")
            for finding in all_findings:
                print(f"\nRow {finding['Row']}:")
                print(f"Pattern: {finding['Pattern']}")
                print(f"Source: {finding['Source IP']} ({finding['Source Network']})")
                print(f"Destination: {finding['Destination IP']} ({finding['Destination Network']})")
                print(f"Services: {finding['Services']}")

    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    analyze_firewall_rules("modified_firewall_updated.xlsx")
