"""
Firewall Rule Checker - Source Any to Specific Destination Analysis
Analyzes firewall rules with any source to specific destination configurations.

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

class SourceAnyDestSpecificAnalyzer:
    """Analyzes firewall rules with any source to specific destination."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.firewall_path = self.base_dir / 'modified_firewall_updated.xlsx'
        self.output_path = self.base_dir / 'output_Source-Any--Destination-Specific--Services-Any-Specific.xlsx'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"source_any_dest_specific_analyzer_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SourceAnyDestSpecificAnalyzer")

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

    def has_specific_value(self, value: Optional[str]) -> bool:
        """Check if there's at least one specific (non-any) value in the field."""
        if pd.isna(value) or not str(value).strip():
            return False
        
        value_str = str(value).replace(';', '\n')
        lines = [line.strip() for line in value_str.split('\n') if line.strip()]
        
        # Check if ANY line is not an "any" value
        return any(not self.is_any_value(line) for line in lines)

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
        """Analyze rules for any source to specific destination patterns."""
        findings = []
        total_rules = len(rules_df)
        
        for index, row in rules_df.iterrows():
            try:
                if index % 100 == 0:
                    self.logger.info(f"Processing rule {index + 1}/{total_rules}")
                
                source = str(row['Source'])
                destination = str(row['Destination'])
                service = str(row.get('Service', 'N/A'))
                
                # Check conditions:
                # 1. Source must be 'any'
                # 2. Destination must have at least one specific (non-any) value
                if self.is_all_any(source) and self.has_specific_value(destination):
                    findings.append({
                        "Row Number": index + 2,  # Excel row number (1-based + header)
                        "Rule Name": row.get('Rule', 'N/A'),
                        "Source": source,
                        "Destination": destination,
                        "Service": service,
                        "Risk Level": "Medium",
                        "Finding": "Rule allows any source to specific destination",
                        "Recommendation": "Review if broad source access is required"
                    })
                    
            except Exception as e:
                self.logger.error(f"Error analyzing rule at row {index + 2}: {str(e)}")
                continue
        
        self.logger.info(f"Analysis complete. Found {len(findings)} rules with any source to specific destination.")
        return findings

    def save_findings(self, findings: List[Dict]) -> None:
        """Save analysis findings to Excel file."""
        if not findings:
            self.logger.info("No findings to save")
            return

        try:
            findings_df = pd.DataFrame(findings)
            
            # Sort findings by risk level and row number
            findings_df['Risk Level'] = pd.Categorical(findings_df['Risk Level'], 
                                                     categories=['High', 'Medium', 'Low'], 
                                                     ordered=True)
            findings_df = findings_df.sort_values(['Risk Level', 'Row Number'])
            
            # Save to Excel with formatting
            with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
                findings_df.to_excel(writer, index=False, sheet_name='Findings')
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Findings']
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            self.logger.info(f"Findings saved to {self.output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving findings: {str(e)}")

    def display_findings(self, findings: List[Dict]) -> None:
        """Display findings in a formatted table."""
        if findings:
            findings_df = pd.DataFrame(findings)
            findings_df['Risk Level'] = pd.Categorical(findings_df['Risk Level'], 
                                                     categories=['High', 'Medium', 'Low'], 
                                                     ordered=True)
            findings_df = findings_df.sort_values(['Risk Level', 'Row Number'])
            
            # Display summary statistics
            print("\nAnalysis Summary:")
            print(f"Total rules analyzed: {len(findings)}")
            risk_summary = findings_df['Risk Level'].value_counts().sort_index()
            for risk_level, count in risk_summary.items():
                print(f"{risk_level} risk findings: {count}")
            
            # Display detailed findings
            print("\nDetailed Findings:")
            print(tabulate(findings_df, headers='keys', tablefmt='grid', showindex=False))
            
            # Display recommendations
            print("\nRecommendations:")
            print("1. Review all rules with 'any' source to ensure they are necessary")
            print("2. Consider implementing more specific source restrictions where possible")
            print("3. Monitor these rules closely for potential security risks")
        else:
            print("No findings to report.")

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
            
            # Save and display results
            self.save_findings(findings)
            self.display_findings(findings)

            return True

        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return False

    def cleanup(self) -> None:
        """Cleanup any temporary resources."""
        try:
            # Add any cleanup code here if needed
            pass
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")

def main():
    """Main execution function."""
    try:
        analyzer = SourceAnyDestSpecificAnalyzer()
        
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
    finally:
        analyzer.cleanup()

if __name__ == "__main__":
    exit(main())
