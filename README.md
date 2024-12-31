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
5. [Contributing](#contributing)
6. [License](#license)

---

## Prerequisites:
Before running the **Firewall Rule Checker** script, ensure you have the following installed:

- **Python 3.x**: Ensure you have Python 3.6 or higher installed.
- **Required Python Libraries**: The script depends on some Python libraries. To install them, run:
  ```bash
  pip install -r requirements.txt

## usage:
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




## Contributing:

We welcome contributions to the **Firewall Rule Checker**! Please follow these steps:

### Step-by-Step Contribution Process:

1. **Fork the repository and create a new branch:**
   - **Command:**
     ```bash
     git checkout -b feature-branch
     ```
   - This creates a new branch for your feature or bug fix. Make sure to replace `feature-branch` with a meaningful name for your branch that describes the changes you're working on.

2. **Make your changes and commit them:**
   - **Command:**
     ```bash
     git commit -m 'Add new feature'
     ```
   - After making your changes to the code, use this command to commit them. Write a clear and concise commit message that describes the changes you've made. For example, `'Add validation for address objects'`.

3. **Push to your fork:**
   - **Command:**
     ```bash
     git push origin feature-branch
     ```
   - Push the changes you made in your branch to your forked repository.

4. **Create a Pull Request:**
   - Go to the repository page on GitHub.
   - You should see an option to create a "Pull Request" (PR) from your branch.
   - Provide a description of the changes you've made, and submit the PR for review.

### Note:
Before contributing, please ensure you have tested the changes locally and that they do not break the existing functionality. It’s important that the code you’re submitting works as intended and does not introduce any errors.



## contact:
  name: "Vishal Patil"
  email: "vp26781@gmail.com"
