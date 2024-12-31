import ipaddress

def extract_ips_from_subnet(subnet):
    ip_network = ipaddress.IPv4Network(subnet, strict=False)
    # Include the first and last IPs along with the hosts
    all_ips = [str(ip_network.network_address)] + [str(ip) for ip in ip_network.hosts()] + [str(ip_network.broadcast_address)]
    return all_ips

def expand_ip_range(ip_range):
    # Split the IP and the range
    ip_part, range_part = ip_range.split('-')
    base_ip = ipaddress.IPv4Address(ip_part)
    start = int(range_part)
    
    # Generate the list of IPs from base_ip to base_ip + start - 1
    return [str(base_ip + i) for i in range(start)]  # No +1, to exclude the last IP

def process_file(input_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    unique_ips = set()  # Use a set to store unique IPs and subnets

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        if '-' in line:  # Check if the line contains an IP range
            try:
                ips = expand_ip_range(line)
                unique_ips.add(line)  # Add the original range
                unique_ips.update(ips)  # Add the expanded IPs
            except ValueError:
                continue  # Skip invalid ranges
        else:  # Assume it's a subnet
            try:
                ips = extract_ips_from_subnet(line)
                unique_ips.add(line)  # Add the original subnet
                unique_ips.update(ips)  # Add the extracted IPs
            except ValueError:
                continue  # Skip invalid subnets

    # Write the unique output back to the same file
    with open(input_file, 'w') as outfile:
        outfile.write('\n'.join(sorted(unique_ips)) + '\n')  # Sort for consistent output

if __name__ == "__main__":
    files_to_process = ['cde.txt', 'oos.txt']
    
    for file in files_to_process:
        process_file(file)
