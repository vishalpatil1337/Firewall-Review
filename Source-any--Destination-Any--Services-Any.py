"""
Firewall Rule Checker - Any Source/Destination/Service Analysis
Analyzes firewall rules to identify rules with "any" values in critical fields.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from tabulate import tabulate

class AnyRuleAnalyzer:
    """Analyzes firewall rules for 'any' values in source, destination, and service fields."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.firewall_path = self.base_dir / 'modified_firewall_updated.xlsx'
        self.output_path = self.base_dir / 'output_Source-Any--Destination-Any--Services-Any.xlsx'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"any_rule_analyzer_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AnyRuleAnalyzer")

    def normalize_value(self, value: Optional[str]) -> str:
        """Normalize the value by converting to lowercase and removing extra whitespace."""
        return str(value).lower().strip() if value is not None else ""

    def is_any_value(self, item: str) -> bool:
        """
        Check if a single item represents 'any'.
        Uses regex to match any text in brackets followed by 'any'.
        """
        item = self.normalize_value(item)
        patterns = [
            '^any$',  # Exactly "any"
            r'^\[.*?\]\s*any$',  # Anything in brackets followed by "any"
            '^$'  # Empty string
        ]
        return any(re.match(pattern, item) for pattern in patterns)

    def is_all_any(self, value: Optional[str]) -> bool:
        """
        Check if all values in the field represent 'any'.
        Returns True if the field is empty, contains only 'any' values, or variations of 'any'.
        """
        # Handle empty/NaN values
        if pd.isna(value) or not str(value).strip():
            return True
        
        # Convert the value to string and normalize newlines and semicolons
        value_str = str(value).replace(';', '\n')
        
        # Split into lines and filter out empty lines
        lines = [line.strip() for line in value_str.split('\n') if line.strip()]
        
        # If all lines are empty, consider it as "any"
        if not lines:
            return True
        
        # Check if ALL lines are "any" values
        return all(self.is_any_value(line) for line in lines)

    def load_firewall_rules(self) -> Optional[pd.DataFrame]:
        """Load and validate firewall rules."""
        try:
            self.logger.info(f"Loading firewall rules from {self.firewall_path}")
            rules_df = pd.read_excel(self.firewall_path)
            
            # Validate required columns
            required_columns = ['Source', 'Destination', 'Service']
            missing_columns = [col for col in required_columns if col not in rules_df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Remove duplicates and empty rows
            rules_df = rules_df.dropna(subset=required_columns, how='all').drop_duplicates()
            
            self.logger.info(f"Loaded {len(rules_df)} rules")
            return rules_df
            
        except Exception as e:
            self.logger.error(f"Error loading firewall rules: {str(e)}")
            return None

    def analyze_rules(self, rules_df: pd.DataFrame) -> List[Dict]:
        """Analyze rules for 'any' values in critical fields."""
        findings = []
        
        for index, row in rules_df.iterrows():
            try:
                source = str(row['Source'])
                destination = str(row['Destination'])
                service = str(row.get('Service', 'N/A'))
                
                # Check conditions: All fields must be 'any'
                if self.is_all_any(source) and self.is_all_any(destination) and self.is_all_any(service):
                    findings.append({
                        "Row Number": index + 2,  # Excel row number (1-based + header)
                        "Rule Name": row.get('Rule', 'N/A'),
                        "Source": source,
                        "Destination": destination,
                        "Service": service,
                        "Risk Level": "High",
                        "Finding": "Rule allows unrestricted access (any-any-any)"
                    })
                    
            except Exception as e:
                self.logger.error(f"Error analyzing rule at row {index + 2}: {str(e)}")
                continue
        
        return findings

    def save_findings(self, findings: List[Dict]) -> None:
        """Save analysis findings to Excel file."""
        if not findings:
            self.logger.info("No findings to save")
            return

        try:
            findings_df = pd.DataFrame(findings)
            
            # Sort by Row Number
            findings_df = findings_df.sort_values('Row Number')
            
            # Save to Excel
            findings_df.to_excel(self.output_path, index=False)
            self.logger.info(f"Findings saved to {self.output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving findings: {str(e)}")

    def display_findings(self, findings: List[Dict]) -> None:
        """Display findings in a formatted table."""
        if findings:
            findings_df = pd.DataFrame(findings)
            print("\nFindings (Rules with any-any-any configuration):")
            print(tabulate(findings_df, headers='keys', tablefmt='grid', showindex=False))
            print(f"\nTotal findings: {len(findings)}")
        else:
            print("No 'any-any-any' rules found.")

    def analyze(self) -> bool:
        """Main analysis method."""
        try:
            # Load rules
            rules_df = self.load_firewall_rules()
            if rules_df is None:
                return False

            # Analyze rules
            self.logger.info("Starting rule analysis...")
            findings = self.analyze_rules(rules_df)
            self.logger.info(f"Analysis complete. Found {len(findings)} any-any-any rules.")

            # Save and display results
            self.save_findings(findings)
            self.display_findings(findings)

            return True

        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        analyzer = AnyRuleAnalyzer()
        
        if analyzer.analyze():
            print("\nAnalysis completed successfully.")
            return 0
        else:
            print("\nAnalysis failed. Check logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
