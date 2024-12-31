project_title: "Firewall Rule Checker"

description: 
  The **Firewall Rule Checker** is an automated Python-based script designed to execute multiple steps for validating and modifying firewall configurations. The script facilitates the execution of various Python modules in sequence, including tasks such as checking firewall rules, replacing address objects, and performing firewall analysis. This tool is ideal for network security professionals who need to streamline firewall rule checking and configuration modification processes.

table_of_contents:
  - "Prerequisites"
  - "Installation Instructions"
  - "Usage"
  - "Script Steps"
  - "Contributing"
  - "License"

prerequisites:
  python_version: "Python 3.x (Python 3.6 or higher)"
  libraries_required:
    - "list of required Python libraries"  # Add the required libraries here
  other_dependencies:
    - "Ensure other scripts (startup.py, format-changer.py, etc.) are in the same directory or update file paths as necessary."

installation_instructions:
  - step_1: "Clone the repository using the following Git command:"
    command: "git clone https://github.com/yourusername/firewall-rule-checker.git"
  - step_2: "Navigate to the project folder:"
    command: "cd firewall-rule-checker"
  - step_3: "Install the necessary dependencies:"
    command: "pip install -r requirements.txt"

usage:
  running_script:
    step_1: "Open the command line or terminal."
    step_2: "Navigate to the project directory:"
      command: "cd firewall-rule-checker"
    step_3: "Execute the script:"
      command: "python firewall-rule-checker.py"
  script_flow: |
    - The script will guide you through various steps.
    - For each step, you’ll be asked to confirm if you wish to proceed by typing 'y' or 'n'.
    - Logs and outputs will be generated, such as `Findings.xlsx`, `firewall_analysis_results.xlsx`, based on your input files and configurations.

script_steps:
  - name: "startup.py"
    description: "Initializes the firewall configuration and generates the required text files and folders (cde.txt, oos.txt, etc.)."
  - name: "format-changer.py"
    description: "Converts firewall CSV files into Excel format."
  - name: "all-in-one.maker-groups.py"
    description: "Combines multiple groups into a single group."
  - name: "replace.py"
    description: "Checks and replaces group names in the firewall configuration."
  - name: "replace-ao.py"
    description: "Updates address objects in the modified firewall file."
  - name: "Source and Destination Rules Check"
    description: "Verifies various firewall rules like Source-Any, Destination-Any, and more."
  - name: "cde-oos-subnet-extractor.py"
    description: "Converts subnet ranges into IP addresses."
  - name: "CDE-OOS-Checker"
    description: "Validates CDE and OOS rules from an Excel file."
  - name: "external-to-internal.py"
    description: "Checks public-to-private firewall rules and generates analysis reports."
  - note: "Each script is executed in sequence, with confirmation prompts to ensure the user is ready for the next step."

contributing:
  steps:
    - step_1: "Fork the repository and create a new branch:"
      command: "git checkout -b feature-branch"
    - step_2: "Make your changes and commit them:"
      command: "git commit -m 'Add new feature'"
    - step_3: "Push to your fork:"
      command: "git push origin feature-branch"
    - step_4: "Create a Pull Request."
  note: "Before contributing, please ensure you have tested the changes locally and that they don’t break the existing functionality."


contact:
  name: "Vishal Patil"
  email: "vp26781@gmail.com"
