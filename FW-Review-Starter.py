import os
import subprocess
import time
from colorama import init, Fore, Style, Back
from typing import Optional

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class FirewallChecker:
    """
    A comprehensive tool for checking and analyzing firewall rules.
    Provides a step-by-step interface for executing various firewall analysis scripts.
    """

    def __init__(self):
        self.scripts_info = {
            "startup.py": "Initializes firewall configuration and generates text files (cde.txt, oos.txt)",
            "format-changer.py": "Converts firewall CSV files into Excel format",
            "all-in-one-maker-groups.py": "Combines multiple groups into a single group",
            "replace.py": "Checks and replaces group names in the firewall configuration",
            "replace-ao.py": "Updates address objects in the modified firewall file",
            "Source-any--Destination-Any--Services-Any.py": "Checks rules with any source, destination, and service",
            "Source-Any--Destination-Specific--Services-Any-Specific.py": "Validates specific destination and service rules",
            "Source-Specific--Destination-Any--Services-Any-Specific.py": "Validates specific source and service rules",
            "Source-Specific--Destination-Specific--Services-Any.py": "Checks rules with specific source and destination",
            "cde-oos-subnet-extractor.py": "Converts subnet ranges into IP addresses",
            "CDE-OOS-Checker.py": "Validates CDE and OOS rules from Excel file",
            "cde-to-external.py": "Checks CDE source to external destination and vice versa",
            "external-to-internal.py": "Analyzes public-to-private firewall rules",
            "formating-findings.py": "Formats the analysis findings",
            "formating-firewall_analysis_results.py": "Formats final analysis results"
        }

    def print_header(self, text: str, style: str = "main") -> None:
        """
        Prints a formatted header with different styles.
        
        Args:
            text: The text to be displayed in the header
            style: The style of header ('main' or 'sub')
        """
        width = 70
        if style == "main":
            print(f"\n{Fore.CYAN + Style.BRIGHT}")
            print("╔" + "═" * (width - 2) + "╗")
            print(f"║{text.center(width - 2)}║")
            print("╚" + "═" * (width - 2) + "╝")
            print(Style.RESET_ALL)
        else:
            print(f"\n{Fore.GREEN + Style.BRIGHT}{'─' * width}")
            print(text.center(width))
            print(f"{'─' * width}{Style.RESET_ALL}\n")

    def execute_script(self, script_name: str) -> bool:
        """
        Executes a Python script and displays its status.
        
        Args:
            script_name: Name of the script to execute
            
        Returns:
            bool: True if execution was successful, False otherwise
        """
        try:
            print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Executing: {Fore.CYAN}{script_name}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Purpose: {self.scripts_info.get(script_name, 'No description available')}")
            subprocess.run(["python", script_name], check=True)
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {script_name} completed successfully\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to execute {script_name}: {e}\n")
            return False

    def confirm_action(self, message: str) -> bool:
        """
        Displays a message and asks for user confirmation.
        
        Args:
            message: The message to display to the user
            
        Returns:
            bool: True if user wants to execute the script, False if they want to skip
        """
        self.print_header(message, "sub")
        while True:
            user_input = input(f"{Fore.YELLOW}Do you want to proceed? [y/n]:{Style.RESET_ALL} ").strip().lower()
            if user_input in ['y', 'n']:
                return user_input == 'y'
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid input. Please enter 'y' or 'n'.")

    def run(self) -> None:
        """Main execution flow of the Firewall Checker tool."""
        self.print_header("Firewall Rule Checker Tool", "main")
        
        steps = [
            ("startup.py", "Step 1: Executing startup.py..."),
            (None, "Step 2: Enter Firewall files in proper format..."),
            ("format-changer.py", "Step 3: Executing format-changer.py..."),
            (None, "Step 4: Open Address Object, remove Table row if present..."),
            ("all-in-one-maker-groups.py", "Step 5: Executing all-in-one-maker-groups.py..."),
            (None, "Step 6: Open all-in-one excel file and remove table column..."),
            ("replace.py", "Step 7: Executing replace.py..."),
            (None, "Step 8: Check modified generated firewall file..."),
            ("replace-ao.py", "Step 9: Executing replace-ao.py..."),
            (None, "Step 10: Check modified generated firewall file..."),
            (None, "Step 11: Checking all Firewall Common Rules..."),
            (None, "Step 12: Checking Source-any--Destination-Any--Services-Any Rule..."),
            ("Source-any--Destination-Any--Services-Any.py", "Step 13: Executing Source-any--Destination-Any--Services-Any.py..."),
            (None, "Step 14: Checking Source-Any--Destination-Specific--Services-Any-Specific Rule..."),
            ("Source-Any--Destination-Specific--Services-Any-Specific.py", "Step 15: Executing Source-Any--Destination-Specific--Services-Any-Specific.py..."),
            (None, "Step 16: Checking Source-Specific--Destination-Any--Services-Any-Specific Rule..."),
            ("Source-Specific--Destination-Any--Services-Any-Specific.py", "Step 17: Executing Source-Specific--Destination-Any--Services-Any-Specific.py..."),
            (None, "Step 18: Checking Source-Specific--Destination-Specific--Services-Any Rule..."),
            ("Source-Specific--Destination-Specific--Services-Any.py", "Step 19: Executing Source-Specific--Destination-Specific--Services-Any.py..."),
            (None, "Step 20: Checking CDE OOS Rules..."),
            ("cde-oos-subnet-extractor.py", "Step 21: Executing cde-oos-subnet-extractor.py..."),
            ("CDE-OOS-Checker.py", "Step 22: Executing CDE-OOS-Checker..."),
            ("cde-to-external.py", "Step 22b: Executing cde-to-external.py..."),
            (None, "Step 23: Findings.xlsx file will be generated, check to find results..."),
            (None, "Step 24: Checking Public-Private rules..."),
            ("external-to-internal.py", "Step 25: Executing external-to-internal.py..."),
            ("formating-findings.py", "Step 25b: Executing formating-findings.py..."),
            ("formating-firewall_analysis_results.py", "Step 25c: Executing formating-firewall_analysis_results.py...")
        ]

        try:
            for script, message in steps:
                execute = self.confirm_action(message)
                
                if script and execute:
                    if not self.execute_script(script):
                        if not self.confirm_action("Script execution failed. Do you want to continue to the next step?"):
                            break
                elif script:
                    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Skipping execution of {script}")
                
                print(f"{Fore.CYAN}[STATUS]{Style.RESET_ALL} Moving to next step...")

            self.print_header("Script is completed. Thanks for using the script!", "main")
            
        except Exception as e:
            print(f"\n{Fore.RED}[CRITICAL ERROR]{Style.RESET_ALL} An unexpected error occurred:")
            print(f"{Fore.RED}{str(e)}{Style.RESET_ALL}")
            print("\nPlease check the error message above and try again.")

if __name__ == "__main__":
    checker = FirewallChecker()
    checker.run()
