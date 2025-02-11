"""
Firewall Rule Checker - Subnet Extractor Tool
Converts subnet ranges into individual IP addresses for CDE and OOS analysis.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import ipaddress
import logging
from typing import List, Set
from pathlib import Path
from datetime import datetime

class SubnetExtractor:
    """Handles extraction of IP addresses from subnets and ranges."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"subnet_extractor_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SubnetExtractor")

    def extract_ips_from_subnet(self, subnet: str) -> Set[str]:
        """
        Extract all IP addresses from a subnet.
        For large networks, only includes network, broadcast, and boundary addresses.
        """
        try:
            ip_network = ipaddress.IPv4Network(subnet, strict=False)
            
            # For large networks, only include network address, broadcast address,
            # and first/last usable addresses
            if ip_network.num_addresses > 1024:
                self.logger.warning(f"Large subnet detected ({subnet}). Including only boundary addresses.")
                return {
                    str(ip_network.network_address),
                    str(ip_network[1]),                    # First usable
                    str(ip_network[-2]),                   # Last usable
                    str(ip_network.broadcast_address)
                }
            
            # For smaller networks, include all addresses
            return {str(ip) for ip in ip_network}
            
        except ValueError as e:
            self.logger.error(f"Invalid subnet {subnet}: {str(e)}")
            return set()

    def expand_ip_range(self, start_ip: str, end_ip: str) -> Set[str]:
        """
        Expand an IP range into individual addresses.
        For large ranges, only includes boundary addresses.
        """
        try:
            start = ipaddress.IPv4Address(start_ip)
            end = ipaddress.IPv4Address(end_ip)
            
            # Check if range is too large
            num_ips = int(end) - int(start) + 1
            if num_ips > 1024:
                self.logger.warning(f"Large IP range detected ({start_ip}-{end_ip}). Including only boundary addresses.")
                return {str(start), str(start + 1), str(end - 1), str(end)}
            
            return {str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)}
            
        except ValueError as e:
            self.logger.error(f"Invalid IP range {start_ip}-{end_ip}: {str(e)}")
            return set()

    def parse_ip_entry(self, line: str) -> Set[str]:
        """Parse an IP entry that could be a subnet or range."""
        line = line.strip()
        if not line:
            return set()
            
        try:
            # Check if it's a range (contains a hyphen)
            if '-' in line:
                start_ip, end_ip = line.split('-')
                return self.expand_ip_range(start_ip.strip(), end_ip.strip())
            else:
                # Treat as a subnet
                return self.extract_ips_from_subnet(line)
                
        except Exception as e:
            self.logger.error(f"Error processing line '{line}': {str(e)}")
            return set()

    def validate_ip(self, ip: str) -> bool:
        """Validate an IP address."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def process_file(self, input_file: Path) -> bool:
        """Process a single input file."""
        try:
            self.logger.info(f"Processing file: {input_file}")
            
            # Read existing entries
            if not input_file.exists():
                self.logger.error(f"File not found: {input_file}")
                return False
                
            with open(input_file, 'r') as infile:
                lines = [line.strip() for line in infile if line.strip()]
            
            # Process each line
            unique_ips = set()
            original_entries = set()
            
            for line in lines:
                self.logger.debug(f"Processing entry: {line}")
                # Keep original entry
                original_entries.add(line)
                
                # Extract and validate IPs
                extracted_ips = self.parse_ip_entry(line)
                valid_ips = {ip for ip in extracted_ips if self.validate_ip(ip)}
                
                if not valid_ips and extracted_ips:
                    self.logger.warning(f"No valid IPs found in entry: {line}")
                
                unique_ips.update(valid_ips)
            
            # Combine original entries and expanded IPs
            all_entries = sorted(original_entries.union(unique_ips))
            
            # Write back to file
            with open(input_file, 'w') as outfile:
                outfile.write('\n'.join(all_entries) + '\n')
            
            self.logger.info(f"Processed {len(lines)} entries into {len(all_entries)} unique IPs/ranges")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing file {input_file}: {str(e)}")
            return False

    def verify_results(self, file_path: Path) -> bool:
        """Verify the results of the processing."""
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
            
            # Verify each line is a valid IP or subnet
            invalid_entries = []
            for line in lines:
                try:
                    if '-' in line:
                        start, end = line.split('-')
                        ipaddress.ip_address(start.strip())
                        ipaddress.ip_address(end.strip())
                    else:
                        ipaddress.ip_network(line, strict=False)
                except ValueError:
                    invalid_entries.append(line)
            
            if invalid_entries:
                self.logger.error(f"Invalid entries found in {file_path}:")
                for entry in invalid_entries:
                    self.logger.error(f"  - {entry}")
                return False
            
            self.logger.info(f"Verification successful for {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying {file_path}: {str(e)}")
            return False

    def process_all_files(self) -> bool:
        """Process both CDE and OOS files."""
        files_to_process = ['cde.txt', 'oos.txt']
        success = True
        
        for filename in files_to_process:
            file_path = self.base_dir / filename
            self.logger.info(f"Processing {filename}...")
            
            if not self.process_file(file_path):
                self.logger.error(f"Failed to process {filename}")
                success = False
                continue
                
            if not self.verify_results(file_path):
                self.logger.error(f"Verification failed for {filename}")
                success = False
                continue
                
            self.logger.info(f"Successfully processed {filename}")
        
        return success

def main():
    """Main execution function."""
    try:
        extractor = SubnetExtractor()
        if extractor.process_all_files():
            print("Subnet extraction completed successfully.")
            return 0
        else:
            print("Subnet extraction failed. Check logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
