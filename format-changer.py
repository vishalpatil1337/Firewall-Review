"""
Firewall Rule Checker - File Format Converter
Converts CSV files to XLSX format and handles file renaming operations.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import os
import logging
import pandas as pd
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime

class FormatConverter:
    """Handles conversion of CSV files to XLSX format and file renaming operations."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.fw_folder = self.base_dir / 'FW'
        self.ao_folder = self.base_dir / 'Address Objects'

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"format_converter_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("FormatConverter")

    def verify_folders(self) -> bool:
        """Verify required folders exist."""
        if not self.fw_folder.exists() or not self.ao_folder.exists():
            self.logger.error("Required folders not found")
            return False
        return True

    def convert_csv_to_xlsx(self, folder_path: Path, new_file_name: str) -> bool:
        """
        Convert CSV file to XLSX format or rename existing XLSX file.
        
        Args:
            folder_path: Path to the folder containing the files
            new_file_name: Desired name for the output XLSX file
            
        Returns:
            bool: True if operation was successful, False otherwise
        """
        try:
            self.logger.info(f"Processing folder: {folder_path}")
            
            # List all relevant files
            csv_files = list(folder_path.glob('*.csv'))
            xlsx_files = list(folder_path.glob('*.xlsx'))
            
            # Process CSV files first
            if csv_files:
                csv_file = csv_files[0]
                self.logger.info(f"Converting CSV file: {csv_file}")
                
                # Read CSV with robust error handling
                try:
                    df = pd.read_csv(csv_file, encoding='utf-8')
                except UnicodeDecodeError:
                    self.logger.warning("UTF-8 encoding failed, trying with latin-1")
                    df = pd.read_csv(csv_file, encoding='latin-1')
                
                # Save as XLSX
                xlsx_path = folder_path / new_file_name
                df.to_excel(xlsx_path, index=False)
                
                # Remove original CSV
                csv_file.unlink()
                self.logger.info(f"Converted {csv_file.name} to {new_file_name}")
                return True
                
            # Handle existing Excel files
            elif xlsx_files:
                for excel_file in xlsx_files:
                    if excel_file.name != new_file_name:
                        new_path = folder_path / new_file_name
                        excel_file.rename(new_path)
                        self.logger.info(f"Renamed {excel_file.name} to {new_file_name}")
                        return True
                self.logger.info(f"File {new_file_name} already exists")
                return True
                
            else:
                self.logger.warning(f"No CSV or Excel files found in {folder_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error processing {folder_path}: {str(e)}")
            return False

    def process_all_folders(self) -> bool:
        """Process all folders and convert/rename files as needed."""
        try:
            if not self.verify_folders():
                return False
            
            # Process FW folder
            fw_success = self.convert_csv_to_xlsx(self.fw_folder, 'firewall.xlsx')
            
            # Process Address Objects folder
            ao_success = self.convert_csv_to_xlsx(self.ao_folder, 'rules.xlsx')
            
            return fw_success and ao_success
            
        except Exception as e:
            self.logger.error(f"Error during folder processing: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        converter = FormatConverter()
        success = converter.process_all_folders()
        
        if success:
            print("File format conversion completed successfully.")
            return 0
        else:
            print("File format conversion failed. Check logs for details.")
            return 1
            
    except Exception as e:
        print(f"Critical error during format conversion: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
