"""
Firewall Rule Checker - Project Initialization Script
Creates necessary folders and files for the firewall analysis project.

Author: Vishal Patil
Email: vp26781@gmail.com
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

class ProjectInitializer:
    """Handles initialization of project structure and required files."""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.required_folders = ["Address Objects", "FW", "Groups"]
        self.required_files = ["cde.txt", "oos.txt"]

    def setup_logging(self) -> None:
        """Configure logging with both file and console output."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"startup_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ProjectInitializer")

    def create_folders(self) -> None:
        """Create required project folders if they don't exist."""
        self.logger.info("Creating required folders...")
        
        for folder in self.required_folders:
            folder_path = self.base_dir / folder
            try:
                folder_path.mkdir(exist_ok=True)
                self.logger.info(f"Created/verified folder: {folder}")
            except Exception as e:
                self.logger.error(f"Failed to create folder '{folder}': {e}")
                raise

    def create_files(self) -> None:
        """Create required project files if they don't exist."""
        self.logger.info("Creating required files...")
        
        for file in self.required_files:
            file_path = self.base_dir / file
            try:
                # Create file if it doesn't exist, leave existing files unchanged
                if not file_path.exists():
                    file_path.touch()
                    self.logger.info(f"Created file: {file}")
                else:
                    self.logger.info(f"File already exists: {file}")
            except Exception as e:
                self.logger.error(f"Failed to create file '{file}': {e}")
                raise

    def verify_structure(self) -> bool:
        """Verify that all required folders and files exist."""
        self.logger.info("Verifying project structure...")
        
        # Check folders
        for folder in self.required_folders:
            if not (self.base_dir / folder).is_dir():
                self.logger.error(f"Required folder missing: {folder}")
                return False
        
        # Check files
        for file in self.required_files:
            if not (self.base_dir / file).is_file():
                self.logger.error(f"Required file missing: {file}")
                return False
        
        self.logger.info("Project structure verification successful")
        return True

    def initialize(self) -> bool:
        """Main initialization method."""
        try:
            self.logger.info("Starting project initialization")
            
            # Create project structure
            self.create_folders()
            self.create_files()
            
            # Verify everything was created correctly
            if not self.verify_structure():
                self.logger.error("Project initialization failed verification")
                return False
            
            self.logger.info("Project initialization completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Project initialization failed: {str(e)}")
            return False

def main():
    """Main execution function."""
    try:
        initializer = ProjectInitializer()
        success = initializer.initialize()
        
        if success:
            print("Project initialization completed successfully.")
            return 0
        else:
            print("Project initialization failed. Check logs for details.")
            return 1
            
    except Exception as e:
        print(f"Critical error during initialization: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
