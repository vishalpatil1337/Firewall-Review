# Firewall Rule Checker

## Project Title: **Firewall Rule Checker**

## Description:
The **Firewall Rule Checker** is an automated Python-based script designed to execute multiple steps for validating and modifying firewall configurations. The script facilitates the execution of various Python modules in sequence, including tasks such as checking firewall rules, replacing address objects, and performing firewall analysis. This tool is ideal for network security professionals who need to streamline firewall rule checking and configuration modification processes. The Firewall Rule Checker automates the process of analyzing firewall configurations to ensure compliance and highlight potential security risks. Below is a description of the rules checked by the script:

## Rule Categories

The framework classifies firewall rules into ten distinct categories to facilitate structured validation.

### 1. **Source-Any to Destination-Any (Services-Any)**
- Identifies unrestricted communication between any source and any destination.
- Flags potential security risks due to lack of restrictions.
- Ensures proper segmentation and access control.

### 2. **Source-Specific to Destination-Any (Services-Any/Specific)**
- Validates specific source IPs/subnets communicating with any destination.
- Ensures comprehensive source IP validation.
- Covers both general and specific service configurations.

### 3. **Source-Specific to Destination-Specific (Services-Any)**
- Verifies communication between specific source and destination IPs.
- Ensures granular service-level access control.
- Checks independent service rule configurations.

### 4. **Source-Any to Destination-Specific (Services-Any/Specific)**
- Analyzes rules where source access is unrestricted.
- Identifies potential security vulnerabilities.
- Assesses destination-specific service access.

### 5. **Out of Scope Source to CDE Destination**
- Flags unauthorized access to the Cardholder Data Environment (CDE).
- Prevents unauthorized data exposure and potential breaches.
- Restricts access across network zones.

### 6. **CDE Destination to Out of Scope Source**
- Identifies risky outbound access from CDE to out-of-scope sources.
- Enforces strict data protection policies.
- Analyzes inbound/outbound CDE traffic for security gaps.

### 7. **CDE Source to External Destination and Vice Versa**
- Monitors communication between the CDE and external networks.
- Ensures compliance with strict data protection protocols.
- Validates both inbound and outbound access control measures.

### 8. **External IP or Subnet to Internal IP or Subnet**
- Validates communication between external and internal networks.
- Ensures robust network segmentation.
- Assesses perimeter security controls.

### 9. **Internal IP or Subnet to External IP or Subnet**
- Examines private network traffic directed towards public networks.
- Mitigates data leakage risks.
- Controls outbound traffic to prevent unauthorized transmissions.

### 10. **Overly Permissive Rules**
- Identifies rules with unrestricted access configurations.
- Recommends security enhancements to tighten access controls.
- Evaluates rule permissiveness to reduce exposure risks.


## Compliance with PCI DSS

The framework ensures adherence to PCI DSS firewall and router security requirements, including:

Requirement 1.1.7: Documentation of all connections to the cardholder data environment.

Requirement 1.2: Restrict inbound and outbound traffic to only what is necessary.

Requirement 1.3: Prohibit direct public access between external networks and CDE.

Requirement 1.4: Install personal firewall software on devices with direct Internet access.

---

## Table of Contents:
1. [Prerequisites](#prerequisites)
2. [Usage](#usage)
3. [Script Flow](#script-flow)

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
   - **step_1:** "Select the firewall configuration file and generate a report using the Nipper tool"
  ![image](https://github.com/user-attachments/assets/307fd3f8-8b16-4e2e-bd00-b88819713d21)

   - **step_2:** "Save Firewall generated report in HTML and Table to CSV Format"
  ![image](https://github.com/user-attachments/assets/08a54b8a-8e20-4136-b02a-a31fc28a8fca)

  -  **step_3:** "After choosing Table to CSV option so many options will come like below given screenshot, Choose only All Network Filtering Tables"
 
![image](https://github.com/user-attachments/assets/ed616deb-d207-4be9-a47a-23e853424a97)

  -  **step_4:** "Install all PreRequirements and Execute the script:"
      ```command: "python FW-Review-Starter.py"```
  -  **step_5:** Ensure that in fw.xlsx, column C contains the 'Source,' column D contains the 'Destination,' and column E contains the 'Service.
- **Name:** `FW.xlsx`
- **Format:** Excel Workbook (.xlsx)
- **Required Column Structure:**

| Position | Column | Header | Content | Required |
|----------|--------|---------|----------|-----------|
| C | Column C | Source | Source IP/Network | Yes |
| D | Column D | Destination | Destination IP/Network | Yes |
| E | Column E | Service | Service/Port | Yes |
| Any | Any | Rule ID | Rule Identifier | Optional |

> ⚠️ **Critical**: Column positions (C, D, E) are mandatory and must not be changed

  -  **step_6:** Ensure that cde.txt and oos.txt are filled with subnets or IP addresses

#### CDE Ranges (`cde.txt`)
```plaintext
# Format: One entry per line
10.1.0.0/16
172.16.1.0/24
```

#### OOS Ranges (`oos.txt`)
```plaintext
# Format: One entry per line
192.168.1.0/24
10.2.0.0/16
```
  


  ---

  
## Script Flow:

1. **Step-by-Step Guidance**  
   The script will guide you through various steps, asking for your confirmation to proceed by typing **'y'** (yes) or **'n'** (no) at each stage.

2. **Processing Input Files and Configurations**  
   You will provide input files and configurations that will be processed by the script.

3. **Output Files Generated**  
   Based on your inputs, the script will generate the following `.xlsx` output files:

| File | Purpose | Contents |
|------|---------|----------|
| output_cde-oos-findings.xlsx | CDE/OOS Analysis | Boundary violations |
| output_external_internal.xlsx | Network Analysis | Public/Private communications |
| output_Source-Any--Destination-Any--Services-Any.xlsx | Any Rule Analysis | Unrestricted access patterns |
| output_Source-Any--Destination-Specific--Services-Any-Specific.xlsx | Source Any Analysis | Source access patterns |
| output_Source-Specific--Destination-Any--Services-Any-Specific.xlsx | Destination Any Analysis | Destination access patterns |
| output_Source-Specific--Destination-Specific--Services-Any.xlsx | Service Any Analysis | Service access patterns |

### 2. Supporting Files

| File | Purpose | Contents |
|------|---------|----------|
| all-in-one.xlsx | Group Analysis | Consolidated groups |
| all_rules.xlsx | Complete Analysis | Full rule assessment |
| modified_firewall.xlsx | Processing | Intermediate results |
| modified_firewall_updated.xlsx | Final Rules | Processed configurations |

---

## Script Workflow

| File | Purpose | Contents |
|------|---------|----------|
| CDE-OOS-Checker.py | CDE/OOS Analysis | Boundary violations |
| cde-to-external.py | CDE to External Analysis | CDE to external network communications |
| Source-any--Destination-Any--Services-Any.py | Any Rule Analysis | Unrestricted access patterns |
| Source-Any--Destination-Specific--Services-Any-Specific.py | Source Any Analysis | Source access patterns |
| Source-Specific--Destination-Any--Services-Any-Specific.py | Destination Any Analysis | Destination access patterns |
| Source-Specific--Destination-Specific--Services-Any.py | Service Any Analysis | Service access patterns |
| external-to-internal.py | Network Analysis | Public/Private network analysis |
| all-in-one-maker-groups.py | Group Analysis | Consolidated group information |
| format-changer.py | Format Conversion | Converts CSV to XLSX format |
| formating-findings.py | Findings Formatting | Formats and consolidates findings |
| FW-Review-Starter.py | Rule Analysis | Executes complete analysis workflow |
| startup.py | Initialization | Creates directory structure and initializes files |


Each script executes in sequence, with prompts ensuring proper execution flow.

---

## Troubleshooting Guide

### Common Issues

#### 1. File Errors
- **Issue:** "File not found"
  
  Solution: Check file existence and permissions
  Verify path: ./FW/modified_firewall_updated.xlsx


- **Issue:** "Column not found"
  
  Solution: Verify column positions (C,D,E)
  Check header names exactly match requirements


#### 2. Processing Errors
- **Issue:** "Memory Error"
  
  Solution: Reduce chunk size in analysis
  Close other applications



---

## Contact:
-  name: Vishal Patil
-  email: vp26781@gmail.com
