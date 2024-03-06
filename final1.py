import re
import sys

# Check if correct number of command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python example.py source.txt filetosave.txt")
    sys.exit(1)

source_file = sys.argv[1]
output_file = sys.argv[2]

# Open source file for reading
try:
    with open(source_file, 'r') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Error: {source_file} not found")
    sys.exit(1)

# Regular expression to match IP addresses and subnets
ip_subnet_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'

# Extract IP addresses and subnets, remove duplicates, and sort them
ip_subnets = sorted(set(re.findall(ip_subnet_regex, ''.join(lines))))

# Write sorted and unique IP addresses and subnets to output file
with open(output_file, 'w') as file:
    file.write('\n'.join(ip_subnets))

print(f"Filtered IP addresses and subnets saved to {output_file}")
