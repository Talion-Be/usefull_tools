import re
import json
import sys

# Check if a filename is provided
if len(sys.argv) < 2:
    print("Usage: python3 transform_forward_bloc_for_netbox_dns.py <filename>")
    sys.exit(1)

# Get filename from command-line argument
input_file = sys.argv[1]
output_file = input_file.rsplit(".", 1)[0] + ".json"  # Replace extension with .json

try:
    # Read file content
    with open(input_file, "r") as file:
        data = file.read()

    # Extract zones and forwarders using regex
    pattern = re.findall(r'zone\s+"([^"]+)"\s+in\s+\{.*?forwarders\s+\{\s*([^}]+)\s*\};', data, re.DOTALL)
    
    # Build JSON structure
    domain_forwarded = {}
    
    for domain, forwarders in pattern:
        ip_list = [ip.strip() for ip in forwarders.split(";") if ip.strip()]
        domain_forwarded[domain] = ip_list

    # Create JSON output
    output_json = {"domain_forwarded": domain_forwarded}

    # Write to JSON file
    with open(output_file, "w") as outfile:
        json.dump(output_json, outfile, indent=4)

    print(f"✅ The file {output_file} has been successfully generated.")

except FileNotFoundError:
    print(f"❌ Error: The file '{input_file}' does not exist.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
