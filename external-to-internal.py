import pandas as pd
import ipaddress
import re
from typing import List, Dict, Optional
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'firewall_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

class IPAnalyzer:
    """Class to handle IP address analysis and validation."""
    
    PRIVATE_NETWORKS = [
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16')
    ]
    
    IP_PATTERN = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?:-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))?')
    
    @staticmethod
    def is_private(ip: str) -> bool:
        """
        Check if an IP address is private.
        
        Args:
            ip (str): IP address to check
            
        Returns:
            bool: True if IP is private, False otherwise
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            return any(ip_obj in network for network in IPAnalyzer.PRIVATE_NETWORKS)
        except ValueError:
            logging.warning(f"Invalid IP address: {ip}")
            return False

    @staticmethod
    def extract_ips(ip_string: str) -> List[str]:
        """
        Extract valid IPs and ranges from a string.
        
        Args:
            ip_string (str): String containing IP addresses and ranges
            
        Returns:
            List[str]: List of extracted IP addresses
        """
        matches = IPAnalyzer.IP_PATTERN.findall(ip_string)
        extracted_ips = []
        
        for start_ip, end_ip in matches:
            end_ip = end_ip or start_ip  # If no end IP, use start IP
            
            try:
                if start_ip != end_ip:
                    start_ip_obj = ipaddress.ip_address(start_ip)
                    end_ip_obj = ipaddress.ip_address(end_ip)
                    
                    # Limit range size to prevent memory issues
                    ip_count = int(end_ip_obj) - int(start_ip_obj) + 1
                    if ip_count > 1000:
                        logging.warning(f"IP range too large ({ip_count} IPs) for {start_ip}-{end_ip}")
                        continue
                        
                    extracted_ips.extend(
                        str(ipaddress.ip_address(ip))
                        for ip in range(int(start_ip_obj), int(end_ip_obj) + 1)
                    )
                else:
                    extracted_ips.append(start_ip)
                    
            except ValueError as e:
                logging.error(f"Error processing IP range {start_ip}-{end_ip}: {e}")
                continue
                
        return extracted_ips

    @staticmethod
    def find_public_ip(ip_list: List[str]) -> Optional[str]:
        """
        Find first public IP from a list of IPs.
        
        Args:
            ip_list (List[str]): List of IP addresses
            
        Returns:
            Optional[str]: First public IP found or None
        """
        return next((ip for ip in ip_list if not IPAnalyzer.is_private(ip)), None)

class FirewallRuleAnalyzer:
    """Class to analyze firewall rules for public/private IP patterns."""
    
    def __init__(self):
        self.excel_file = "modified_firewall_updated.xlsx"  # Hardcoded filename
        self.ip_analyzer = IPAnalyzer()
        
    def load_rules(self) -> pd.DataFrame:
        """Load and validate firewall rules from Excel file."""
        try:
            rules_df = pd.read_excel(
                self.excel_file,
                usecols="C,D,E",
                names=['Source', 'Destination', 'Services']
            )
            
            # Basic validation
            if rules_df.empty:
                raise ValueError("No rules found in the Excel file")
            if rules_df.isnull().any().any():
                logging.warning("Found null values in the rules")
                
            return rules_df
            
        except Exception as e:
            logging.error(f"Error loading rules: {e}")
            raise
            
    def analyze_rules(self, rules_df: pd.DataFrame) -> List[Dict]:
        """
        Analyze rules for public/private IP patterns.
        
        Args:
            rules_df (pd.DataFrame): DataFrame containing firewall rules
            
        Returns:
            List[Dict]: List of findings
        """
        findings = []
        total_rules = len(rules_df)
        
        for index, row in rules_df.iterrows():
            logging.info(f"Analyzing rule {index + 2}/{total_rules}")
            
            try:
                source_ips = self.ip_analyzer.extract_ips(row['Source'])
                dest_ips = self.ip_analyzer.extract_ips(row['Destination'])
                
                # Skip empty rules
                if not source_ips or not dest_ips:
                    logging.warning(f"Empty IPs in row {index + 2}")
                    continue
                
                self._check_rule_pattern(
                    index, row, source_ips, dest_ips, findings,
                    not_private_source=True, private_dest=True,
                    rule_type="Public Source to Private Destination"
                )
                
                self._check_rule_pattern(
                    index, row, source_ips, dest_ips, findings,
                    not_private_source=False, private_dest=False,
                    rule_type="Private Source to Public Destination"
                )
                
            except Exception as e:
                logging.error(f"Error analyzing rule at row {index + 2}: {e}")
                continue
                
        return findings
        
    def _check_rule_pattern(
        self, index: int, row: pd.Series, source_ips: List[str], 
        dest_ips: List[str], findings: List[Dict], 
        not_private_source: bool, private_dest: bool, rule_type: str
    ) -> None:
        """Helper method to check specific rule patterns."""
        source_condition = any(
            not self.ip_analyzer.is_private(ip) if not_private_source 
            else self.ip_analyzer.is_private(ip) 
            for ip in source_ips
        )
        
        dest_condition = any(
            self.ip_analyzer.is_private(ip) if private_dest 
            else not self.ip_analyzer.is_private(ip) 
            for ip in dest_ips
        )
        
        if source_condition and dest_condition:
            public_ip = self.ip_analyzer.find_public_ip(
                source_ips if not_private_source else dest_ips
            )
            if public_ip:
                findings.append({
                    "Rule Type": rule_type,
                    "Row Number": index + 2,
                    "Source": row['Source'],
                    "Destination": row['Destination'],
                    "Services": row['Services'],
                    "Public IP": public_ip
                })

    def save_results(self, findings: List[Dict]) -> None:
        """Save analysis results to Excel file."""
        if not findings:
            logging.info("No findings to save")
            return
            
        output_file = "modified_firewall_updated.xlsx"  # Fixed output filename
        
        try:
            findings_df = pd.DataFrame(findings)
            findings_df.to_excel(output_file, index=False)
            logging.info(f"Results saved to {output_file}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            raise

def main():
    """Main function to run the firewall rule analysis."""
    try:
        analyzer = FirewallRuleAnalyzer()
        rules_df = analyzer.load_rules()
        
        logging.info(f"Analyzing {len(rules_df)} rules...")
        findings = analyzer.analyze_rules(rules_df)
        
        if findings:
            logging.info(f"Found {len(findings)} rules matching criteria")
            for finding in findings:
                logging.info(
                    f"{finding['Rule Type']}: Row {finding['Row Number']}, "
                    f"Source: {finding['Source']}, "
                    f"Destination: {finding['Destination']}, "
                    f"Services: {finding['Services']}, "
                    f"Public IP: {finding['Public IP']}"
                )
        else:
            logging.info("No findings reported")
            
        analyzer.save_results(findings)
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()
