"""
Firewall Rule Checker - Group Name Replacement Tool
Replaces group names in firewall configuration with consolidated names.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import os
import re
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

class GroupReplacer:
    """Handles replacement of group names in firewall configuration."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.all_in_one_path = self.base_dir / 'all-in-one.xlsx'
        self.firewall_path = self.base_dir / 'FW' / 'firewall.xlsx'
        self.output_path = self.base_dir / 'modified_firewall.xlsx'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"group_replacer_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("GroupReplacer")

    def load_excel_files(self) -> tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load required Excel files with error handling."""
        all_in_one_df = None
        firewall_df = None
        
        try:
            # Load all-in-one.xlsx
            self.logger.info(f"Loading {self.all_in_one_path}")
            all_in_one_df = pd.read_excel(self.all_in_one_path)
            
            # Validate required columns
            if 'Row A' not in all_in_one_df.columns or 'Row B' not in all_in_one_df.columns:
                raise ValueError("Required columns 'Row A' and 'Row B' not found in all-in-one.xlsx")
            
            # Load firewall.xlsx
            self.logger.info(f"Loading {self.firewall_path}")
            firewall_df = pd.read_excel(self.firewall_path)
            
        except FileNotFoundError as e:
            self.logger.error(f"Required file not found: {e}")
        except Exception as e:
            self.logger.error(f"Error loading Excel files: {e}")
            
        return all_in_one_df, firewall_df

    @staticmethod
    def escape_regex_patterns(replacement_dict: Dict[str, str]) -> Dict[str, str]:
        """Escape special characters in replacement patterns."""
        escaped_dict = {}
        for key, value in replacement_dict.items():
            try:
                escaped_key = re.escape(str(key))
                escaped_dict[escaped_key] = str(value)
            except Exception as e:
                logging.error(f"Error escaping key '{key}': {e}")
                continue
        return escaped_dict

    def create_replacement_dict(self, df: pd.DataFrame) -> Dict[str, str]:
        """Create dictionary for replacements from DataFrame."""
        # Remove any rows with NaN values
        df = df.dropna(subset=['Row A', 'Row B'])
        
        # Create dict with string values
        replacement_dict = dict(zip(df['Row A'].astype(str), df['Row B'].astype(str)))
        
        # Escape special characters
        return self.escape_regex_patterns(replacement_dict)

    def replace_words_in_firewall(self, df: pd.DataFrame, replacements: Dict[str, str]) -> pd.DataFrame:
        """Replace words in the firewall DataFrame with proper error handling."""
        result_df = df.copy()
        
        for col in df.columns:
            try:
                result_df[col] = result_df[col].astype(str).replace(replacements, regex=True)
            except Exception as e:
                self.logger.error(f"Error processing column '{col}': {e}")
                
        return result_df

    def process_files(self) -> bool:
        """Main processing function."""
        try:
            # Load files
            all_in_one_df, firewall_df = self.load_excel_files()
            if all_in_one_df is None or firewall_df is None:
                return False
            
            # Create replacement dictionary
            self.logger.info("Creating replacement dictionary")
            replacement_dict = self.create_replacement_dict(all_in_one_df)
            
            # Process replacements
            self.logger.info("Processing replacements")
            modified_firewall_df = self.replace_words_in_firewall(firewall_df, replacement_dict)
            
            # Save results
            self.logger.info(f"Saving results to {self.output_path}")
            modified_firewall_df.to_excel(self.output_path, index=False)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during processing: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        replacer = GroupReplacer()
        success = replacer.process_files()
        
        if success:
            print("Group replacement completed successfully.")
            return 0
        else:
            print("Group replacement failed. Check logs for details.")
            return 1
            
    except Exception as e:
        print(f"Critical error during replacement: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
