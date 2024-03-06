import re

def extract_ip_subnets(filename):
    # Open the file for reading
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Regular expression to match IP addresses and subnets
    ip_subnet_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'

    # Extract and return IP addresses and subnets
    return sorted(set(re.findall(ip_subnet_regex, ''.join(lines))))

def compare_ip_subnets(file1, file2):
    ip_subnets1 = extract_ip_subnets(file1)
    ip_subnets2 = extract_ip_subnets(file2)

    # Find matching IP addresses and subnets
    matching_ip_subnets = set(ip_subnets1) & set(ip_subnets2)

    return matching_ip_subnets

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python example.py source1.txt source2.txt")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    matching_ip_subnets = compare_ip_subnets(file1, file2)

    print("Matching IP Addresses and Subnets:")
    for ip_subnet in matching_ip_subnets:
        print(ip_subnet)
