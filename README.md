`FIREWALL REVIEW RULES CHECKER`

Project is still under process : 

1) execute startup.py  ( to make FW, Address Objects, Groups, cde.txt. oos.txt )
2) echo "enter Firewall files in proper format" 
3) execute format-changer.py (to convert .csv into .xlsx)
4) echo "open Address Object, remove Table row if present there, open Firewall excel and source should be present on C, Destination on d & services on  E row"
5) execute all-in-one-maker-groups.py (arrange a multiple groups in single group)
6) echo "open all-in-one excel file and remove table column"
7) execute replace.py (to check group names, if value matched with firewall then replace the next value with matched value)
8) echo "check modified generated firewall file"
9) execute replace-ao.py (replace Address Objects value with Modified Firewall file)
10) echo "check modified generated firewall file"
11) echo "Checking all Firewall Common Rules"
12) echo "Checking Source-any--Destination-Any--Services-Any Rule"
13) execute Source-any--Destination-Any--Services-Any.py
14) echo "Checking Source-Any--Destination-Specific--Services-Any-Specific Rule"
15) execute Source-Any--Destination-Specific--Services-Any-Specific.py
16) echo "Checking Source-Specific--Destination-Any--Services-Any-Specific Rule"
17) execute Source-Specific--Destination-Any--Services-Any-Specific.py
18) echo "Checking Source-Specific--Destination-Specific--Services-Any Rule"
19) execute Source-Specific--Destination-Specific--Services-Any.py
20) echo "Checking CDE OOS Rules"
21) execute cde-oos-subnet-extractor.py (to convert subnet into ip address in cde.txt and oos.txt)
22) execute CDE-OOS-Checker (checking CDE OOS rules from excel file)
23) echo "Findings.xlsx file will generated, check to find results"
24) echo "checking Public-Private rules"
25) execute external-to-internal.py (it will check public and private rules and will generate firewall_analysis_results excel file)
26) echo "Script is completed. thanks for using the script"
