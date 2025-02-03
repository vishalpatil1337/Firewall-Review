# Firewall Rule Checker

## Project Title: **Firewall Rule Checker**

## Description:
The **Firewall Rule Checker** is an automated Python-based script designed to execute multiple steps for validating and modifying firewall configurations. The script facilitates the execution of various Python modules in sequence, including tasks such as checking firewall rules, replacing address objects, and performing firewall analysis. This tool is ideal for network security professionals who need to streamline firewall rule checking and configuration modification processes. The Firewall Rule Checker automates the process of analyzing firewall configurations to ensure compliance and highlight potential security risks. Below is a description of the rules checked by the script:

rules_check:
```
- 1. Source-Specific to Destination-Any

Validate specific source IPs/subnets against any destination
Ensure comprehensive source IP validation
Cover specific or any service configurations

- 2. Source-Specific to Destination-Specific

Verify communication between specific source and destination IPs
Validate granular service-level access control
Independent service rule checking

- 3. Source-Any to Destination-Specific

Analyze rules with unrestricted source access
Identify potential security vulnerabilities
Assess destination-specific services

- 4. Out of Scope Source to CDE Destination

Flag unauthorized Cardholder Data Environment (CDE) access
Prevent potential data breaches
Restrict cross-zone access

- 5. CDE Destination to Out of Scope Source

Identify risky CDE access patterns
Enforce strict data protection
Analyze inbound/outbound CDE traffic

- 6. CDE to External Network

Monitor CDE communication with external networks
Validate external access to sensitive environments
Ensure strict data protection protocols

- 7. External to CDE Network

Analyze external network attempts to access CDE
Implement rigorous access control mechanisms
Prevent unauthorized data exposure

- 8. External to Internal Network

Validate public-to-private network communication
Ensure robust network segmentation
Assess perimeter security

- 9. Internal to External Network

Examine private-to-public rules
Mitigate data leakage risks
Control outbound traffic

- 10. Overly Permissive Rules

Identify unrestricted access configurations
Recommend security enhancements
Evaluate rule permissiveness
 ```

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
  pip install prettytable
  pip install colorama

## Usage:
  To run script:
   - step_1: "Select the firewall configuration file and generate a report using the Nipper tool"
  ![image](https://github.com/user-attachments/assets/307fd3f8-8b16-4e2e-bd00-b88819713d21)

   - step_2: "Save Firewall generated report in HTML and Table to CSV Format"
  ![image](https://github.com/user-attachments/assets/08a54b8a-8e20-4136-b02a-a31fc28a8fca)

  -  step_3: "After choosing Table to CSV option so many options will come like below given screenshot, Choose only All Network Filtering Tables"
 
![image](https://github.com/user-attachments/assets/ed616deb-d207-4be9-a47a-23e853424a97)

  -  step_4: "Install all PreRequirements and Execute the script:"
      ```command: "python FW-Review-Starter.py"```
  


  ---

  
  ## Script_Flow: 
    - The script will guide you through various steps.
    - For each step, you’ll be asked to confirm if you wish to proceed by typing 'y' or 'n'.
    - Logs and outputs will be generated, such as `Findings.xlsx`, `firewall_analysis_results.xlsx`, based on your input files and configurations.


---

## Script_Steps:
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


---

## Contact:
-  name: Vishal Patil
-  email: vp26781@gmail.com
