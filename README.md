# README.txt for Firewall Rule Checker

## Project Title: **Firewall Rule Checker**

## Description:
The **Firewall Rule Checker** is an automated Python-based script designed to execute multiple steps for validating and modifying firewall configurations. The script facilitates the execution of various Python modules in sequence, including tasks such as checking firewall rules, replacing address objects, and performing firewall analysis. This tool is ideal for network security professionals who need to streamline firewall rule checking and configuration modification processes.

---

## Table of Contents:
1. [Prerequisites](#prerequisites)
2. [Installation Instructions](#installation-instructions)
3. [Usage](#usage)
4. [Script Steps](#script-steps)

---

## Prerequisites:
Before running the **Firewall Rule Checker** script, ensure you have the following installed:

- **Python 3.x**: Ensure you have Python 3.6 or higher installed.
- **Required Python Libraries**: The script depends on some Python libraries. To install them, run:
  ```bash
  pip install pandas
  pip install openpyxl
  pip install xlsxwriter

## Usage:
  running_script:
    step_1: "Open the command line or terminal."
    step_2: "Navigate to the project directory:"
      command: "cd firewall-review"
    step_3: "Execute the script:"
      ```command: "python FW-Review-Starter.py"```
  
  
  script_flow: |
    - The script will guide you through various steps.
    - For each step, you’ll be asked to confirm if you wish to proceed by typing 'y' or 'n'.
    - Logs and outputs will be generated, such as `Findings.xlsx`, `firewall_analysis_results.xlsx`, based on your input files and configurations.


script_steps:
  - name: "startup.py"          description: "Initializes firewall configuration and generates text files (cde.txt, oos.txt, etc.)"
  - name: "format-changer.py"    description: "Converts firewall CSV files into Excel format"
  - name: "all-in-one.maker-groups.py" description: "Combines multiple groups into a single group"
  - name: "replace.py"           description: "Checks and replaces group names in the firewall configuration"
  - name: "replace-ao.py"        description: "Updates address objects in the modified firewall file"
  - name: "Source and Destination Rules Check" description: "Verifies firewall rules like Source-Any, Destination-Any, and more"
  - name: "cde-oos-subnet-extractor.py" description: "Converts subnet ranges into IP addresses"
  - name: "CDE-OOS-Checker"     description: "Validates CDE and OOS rules from an Excel file"
  - name: "external-to-internal.py" description: "Checks public-to-private firewall rules and generates analysis reports"
  - note: "Each script is executed in sequence, with confirmation prompts to ensure the user is ready for the next step."




## contact:
  name: Vishal Patil
  email: vp26781@gmail.com
