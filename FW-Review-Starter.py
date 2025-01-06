import os
import subprocess
import time

def execute_script(script_name):
    """Execute the provided script and display a message in CMD."""
    print(f"\n[INFO] Executing {script_name}...\n")
    subprocess.run(["python", script_name], check=True)

def echo_message(message):
    """Display a formatted message and ask the user for confirmation."""
    print(f"\n{'='*50}")
    print(f"{message.center(50)}")
    print(f"{'='*50}")
    while True:
        user_input = input("\nDo you want to proceed? [y/n]: ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("\n[ERROR] Invalid input. Please enter 'y' or 'n'.")

def print_separator():
    """Print a separator line for clarity."""
    print("\n" + "="*50 + "\n")

def main():
    print("\n" + "="*50)
    print(f"{'Welcome to the Firewall Rule Checker Script'.center(50)}")
    print("="*50 + "\n")

    # 1. Execute startup.py
    if echo_message("Step 1: Executing startup.py..."):
        execute_script("startup.py")

    # 2. Echo Firewall file format message
    echo_message("Step 2: Enter Firewall files in proper format...")

    # 3. Execute format-changer.py
    if echo_message("Step 3: Executing format-changer.py..."):
        execute_script("format-changer.py")

    # 4. Echo Address Object instructions
    echo_message("Step 4: Open Address Object, remove Table row if present...")

    # 5. Execute all-in-one-maker-groups.py
    if echo_message("Step 5: Executing all-in-one-maker-groups.py..."):
        execute_script("all-in-one-maker-groups.py")

    # 6. Echo all-in-one excel file instructions
    echo_message("Step 6: Open all-in-one excel file and remove table column...")

    # 7. Execute replace.py
    if echo_message("Step 7: Executing replace.py..."):
        execute_script("replace.py")

    # 8. Check modified generated firewall file
    echo_message("Step 8: Check modified generated firewall file...")

    # 9. Execute replace-ao.py
    if echo_message("Step 9: Executing replace-ao.py..."):
        execute_script("replace-ao.py")

    # 10. Check modified generated firewall file
    echo_message("Step 10: Check modified generated firewall file...")

    # 11. Checking all Firewall Common Rules
    echo_message("Step 11: Checking all Firewall Common Rules...")

    # 12. Checking Source-any--Destination-Any--Services-Any Rule
    echo_message("Step 12: Checking Source-any--Destination-Any--Services-Any Rule...")

    # 13. Execute Source-any--Destination-Any--Services-Any.py
    if echo_message("Step 13: Executing Source-any--Destination-Any--Services-Any.py..."):
        execute_script("Source-any--Destination-Any--Services-Any.py")

    # 14. Checking Source-Any--Destination-Specific--Services-Any-Specific Rule
    echo_message("Step 14: Checking Source-Any--Destination-Specific--Services-Any-Specific Rule...")

    # 15. Execute Source-Any--Destination-Specific--Services-Any-Specific.py
    if echo_message("Step 15: Executing Source-Any--Destination-Specific--Services-Any-Specific.py..."):
        execute_script("Source-Any--Destination-Specific--Services-Any-Specific.py")

    # 16. Checking Source-Specific--Destination-Any--Services-Any-Specific Rule
    echo_message("Step 16: Checking Source-Specific--Destination-Any--Services-Any-Specific Rule...")

    # 17. Execute Source-Specific--Destination-Any--Services-Any-Specific.py
    if echo_message("Step 17: Executing Source-Specific--Destination-Any--Services-Any-Specific.py..."):
        execute_script("Source-Specific--Destination-Any--Services-Any-Specific.py")

    # 18. Checking Source-Specific--Destination-Specific--Services-Any Rule
    echo_message("Step 18: Checking Source-Specific--Destination-Specific--Services-Any Rule...")

    # 19. Execute Source-Specific--Destination-Specific--Services-Any.py
    if echo_message("Step 19: Executing Source-Specific--Destination-Specific--Services-Any.py..."):
        execute_script("Source-Specific--Destination-Specific--Services-Any.py")

    # 20. Checking CDE OOS Rules
    echo_message("Step 20: Checking CDE OOS Rules...")

    # 21. Execute cde-oos-subnet-extractor.py
    if echo_message("Step 21: Executing cde-oos-subnet-extractor.py..."):
        execute_script("cde-oos-subnet-extractor.py")

    # 22. Execute CDE-OOS-Checker
    if echo_message("Step 22: Executing CDE-OOS-Checker..."):
        execute_script("CDE-OOS-Checker.py")

    # 23. Finding message
    echo_message("Step 23: Findings.xlsx file will be generated, check to find results...")

    # 24. Checking Public-Private rules
    echo_message("Step 24: Checking Public-Private rules...")

    # 25. Execute external-to-internal.py
    if echo_message("Step 25: Executing external-to-internal.py..."):
        execute_script("external-to-internal.py")
        execute_script("formating-findings.py")
        execute_script("formating-firewall_analysis_results.py")

    # 26. Script completion message
    print_separator()
    print(f"{'Script is completed. Thanks for using the script!'.center(50)}")
    print("="*50)

if __name__ == "__main__":
    main()
