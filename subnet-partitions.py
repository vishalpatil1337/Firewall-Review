import argparse
import ipaddress

def extract_ips_from_subnet(subnet):
    ip_network = ipaddress.IPv4Network(subnet, strict=False)
    return [str(ip) for ip in ip_network.hosts()]

def main(input_file):
    output_file = 'output_ips.txt'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            subnet = line.strip()
            ips = extract_ips_from_subnet(subnet)
            
            # Save IPs in the output file
            outfile.write(f"Subnet: {subnet}\n")
            outfile.write("IPs:\n")
            outfile.write('\n'.join(ips) + '\n\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract IPs from subnets.')
    parser.add_argument('input_file', nargs='?', help='Input file containing subnets (optional)')
    args = parser.parse_args()

    if args.input_file:
        main(args.input_file)
    else:
        input_file = input("Enter the name of the input file: ")
        main(input_file)
