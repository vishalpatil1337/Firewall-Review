"""
Firewall Rule Checker - Group Consolidation Tool
Combines multiple firewall address groups into a consolidated format.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import pandas as pd
import os
import glob
import re
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class GroupConsolidator:
    """Handles consolidation of multiple firewall address groups."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.groups_dir = self.base_dir / 'Groups'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"group_consolidator_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("GroupConsolidator")

    @staticmethod
    def clean_string(s: Optional[str]) -> str:
        """Clean illegal characters from strings."""
        if not isinstance(s, str):
            return str(s) if s is not None else ""
        return re.sub(r'[^\x20-\x7E]', '', s)

    @staticmethod
    def extract_group_name(s: Optional[str]) -> str:
        """Extract the group name from the row."""
        if not isinstance(s, str):
            return str(s) if s is not None else ""
        
        # Remove "Table" followed by numbers and "address group"
        s = re.sub(r'Table \d+ ', '', s)
        s = re.sub(r'address group$', '', s).strip()
        return s

    def verify_groups_folder(self) -> bool:
        """Verify Groups folder exists and contains CSV files."""
        if not self.groups_dir.exists():
            self.logger.error(f"Groups folder not found: {self.groups_dir}")
            return False
            
        csv_files = list(self.groups_dir.glob('*.csv'))
        if not csv_files:
            self.logger.error("No CSV files found in Groups folder")
            return False
            
        return True

    def read_csv_files(self) -> List[pd.DataFrame]:
        """Read and process all CSV files in the Groups folder."""
        dataframes = []
        csv_files = list(self.groups_dir.glob('*.csv'))
        
        for csv_file in csv_files:
            try:
                self.logger.info(f"Processing file: {csv_file.name}")
                
                # Try different encodings
                try:
                    df = pd.read_csv(csv_file, header=None, encoding='utf-8')
                except UnicodeDecodeError:
                    self.logger.warning(f"UTF-8 encoding failed for {csv_file.name}, trying latin-1")
                    df = pd.read_csv(csv_file, header=None, encoding='latin-1')
                
                # Clean data
                df = df.apply(lambda col: col.map(self.clean_string))
                dataframes.append(df)
                
            except Exception as e:
                self.logger.error(f"Error processing {csv_file.name}: {str(e)}")
                continue
                
        return dataframes

    def consolidate_groups(self) -> bool:
        """Consolidate all group data into a single Excel file."""
        try:
            if not self.verify_groups_folder():
                return False
            
            # Read all CSV files
            self.logger.info("Reading CSV files...")
            dataframes = self.read_csv_files()
            
            if not dataframes:
                self.logger.error("No valid data found to consolidate")
                return False
            
            # Concatenate all DataFrames
            self.logger.info("Consolidating data...")
            all_data = pd.concat(dataframes, ignore_index=True)
            
            # Process consolidated data
            consolidated_data = []
            for key, group in all_data.groupby(0):
                group_name = self.extract_group_name(key)
                addresses = ', '.join(group[1].astype(str).unique())  # Use unique to remove duplicates
                consolidated_data.append([group_name, addresses])
            
            # Create final DataFrame
            final_df = pd.DataFrame(consolidated_data, columns=['Row A', 'Row B'])
            
            # Save to Excel
            output_file = self.base_dir / 'all-in-one.xlsx'
            final_df.to_excel(output_file, index=False)
            
            self.logger.info(f"Consolidated data saved to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during consolidation: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        consolidator = GroupConsolidator()
        success = consolidator.consolidate_groups()
        
        if success:
            print("Group consolidation completed successfully.")
            return 0
        else:
            print("Group consolidation failed. Check logs for details.")
            return 1
            
    except Exception as e:
        print(f"Critical error during consolidation: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
