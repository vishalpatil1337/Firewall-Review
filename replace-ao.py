"""
Firewall Rule Checker - Address Object Replacement Tool
Updates address objects in the modified firewall configuration file.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import os
import re
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime

class AddressObjectReplacer:
    """Handles replacement of address objects in firewall configuration."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.rules_path = self.base_dir / 'Address Objects' / 'rules.xlsx'
        self.firewall_path = self.base_dir / 'modified_firewall.xlsx'
        self.output_path = self.base_dir / 'modified_firewall_updated.xlsx'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"address_replacer_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AddressObjectReplacer")

    def load_excel_files(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load and validate Excel files."""
        rules_df = None
        firewall_df = None
        
        try:
            # Load rules.xlsx
            self.logger.info(f"Loading {self.rules_path}")
            rules_df = pd.read_excel(self.rules_path)
            
            # Validate required columns
            if 'Name' not in rules_df.columns or 'Address' not in rules_df.columns:
                raise ValueError("Rules file must contain 'Name' and 'Address' columns")
            
            # Load firewall.xlsx
            self.logger.info(f"Loading {self.firewall_path}")
            firewall_df = pd.read_excel(self.firewall_path)
            
        except FileNotFoundError as e:
            self.logger.error(f"Required file not found: {e}")
        except Exception as e:
            self.logger.error(f"Error loading Excel files: {e}")
            
        return rules_df, firewall_df

    def create_replacement_dict(self, rules_df: pd.DataFrame) -> Dict[str, str]:
        """Create clean replacement dictionary from rules DataFrame."""
        # Drop any rows with null values
        rules_df = rules_df.dropna(subset=['Name', 'Address'])
        
        # Convert both columns to string and strip whitespace
        rules_df['Name'] = rules_df['Name'].astype(str).str.strip()
        rules_df['Address'] = rules_df['Address'].astype(str).str.strip()
        
        # Create dictionary with exact word boundaries
        replacement_dict = dict(zip(rules_df['Name'], rules_df['Address']))
        
        # Validate the dictionary isn't empty
        if not replacement_dict:
            raise ValueError("No valid replacement rules found in rules file")
            
        return replacement_dict

    def replace_words_in_cell(self, cell: str, replacement_dict: Dict[str, str]) -> str:
        """Replace words in a single cell with exact matching."""
        if pd.isna(cell) or not isinstance(cell, str):
            return str(cell)
        
        cell_str = str(cell)
        
        # Perform replacements with word boundaries
        for old_word, new_word in replacement_dict.items():
            pattern = r'\b' + re.escape(old_word) + r'\b'
            cell_str = re.sub(pattern, new_word, cell_str)
        
        return cell_str

    def process_firewall_data(self, firewall_df: pd.DataFrame, replacement_dict: Dict[str, str]) -> pd.DataFrame:
        """Process the firewall DataFrame with replacements."""
        # Create a copy to avoid modifying the original
        result_df = firewall_df.copy()
        
        # Only process string/object columns
        string_columns = result_df.select_dtypes(include=['object']).columns
        
        if not len(string_columns):
            raise ValueError("No string columns found in firewall data to process")
        
        # Apply replacements to each string column
        for col in string_columns:
            self.logger.info(f"Processing column: {col}")
            result_df[col] = result_df[col].apply(lambda x: self.replace_words_in_cell(x, replacement_dict))
        
        return result_df

    def optimize_memory(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage."""
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype('category')
            elif df[col].dtype == 'float64':
                df[col] = pd.to_numeric(df[col], downcast='float')
            elif df[col].dtype == 'int64':
                df[col] = pd.to_numeric(df[col], downcast='integer')
        return df

    def process_files(self) -> bool:
        """Main processing function."""
        try:
            # Load files
            rules_df, firewall_df = self.load_excel_files()
            if rules_df is None or firewall_df is None:
                return False
            
            # Create replacement dictionary
            self.logger.info("Creating replacement dictionary")
            replacement_dict = self.create_replacement_dict(rules_df)
            self.logger.info(f"Found {len(replacement_dict)} replacement rules")
            
            # Process the firewall data
            self.logger.info(f"Processing {len(firewall_df)} rows in firewall data")
            updated_firewall_df = self.process_firewall_data(firewall_df, replacement_dict)
            
            # Optimize memory usage
            updated_firewall_df = self.optimize_memory(updated_firewall_df)
            
            # Save the results
            self.logger.info(f"Saving results to {self.output_path}")
            updated_firewall_df.to_excel(self.output_path, index=False)
            
            self.logger.info("Processing completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during processing: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        replacer = AddressObjectReplacer()
        success = replacer.process_files()
        
        if success:
            print("Address object replacement completed successfully.")
            return 0
        else:
            print("Address object replacement failed. Check logs for details.")
            return 1
            
    except Exception as e:
        print(f"Critical error during replacement: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
