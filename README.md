### 📌 **BIND to JSON Conversion Script Documentation**

This script extracts **DNS zones and their forwarders** from a **BIND configuration file** and converts them into **JSON format**.

---

## 🚀 **Usage**

### 📌 **Prerequisites**

- **Python 3.x** must be installed on your system.
- The input file should be a text file containing **DNS zone configurations**.

### 📌 **Basic Command**

```bash
python3 transform_forward_bloc_for_netbox_dns.py <filename>
```

**Example:**

```bash
python3 transform_forward_bloc_for_netbox_dns.py test.txt
```

This will generate a file named **`test.json`** with the converted data.

---

## 📥 **Example Input (`test.txt`)**

```txt
  zone "amin.nt" in {
    type forward;
    forward only;
    forwarders { 6.2.0.1; 6.2.0.2; };
  };

  zone "eda.org" in {
    type forward;
    forward only;
    forwarders { 6.2.3.2; };
  };

  zone "test.du" in {
    type forward;
    forward only;
    forwarders { 6.2.15.1; 6.2.15.5; 6.2.15.6; 6.2.15.22; };
  };
```

---

## 📤 **Example Output (`test.json`)**

```json
{
    "domain_forwarded": {
        "amin.nt": [
            "6.2.0.1",
            "6.2.0.2"
        ],
        "eda.org": [
            "6.2.3.2"
        ],
        "test.du": [
            "6.2.15.1",
            "6.2.15.5",
            "6.2.15.6",
            "6.2.15.22"
        ]
    }
}
```

---

## 🖥️ **Script Code (`transform_forward_bloc_for_netbox_dns.py`)**

```python
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
```

---

## 🔧 **Error Handling**

| Error                                   | Possible Cause                                              | Solution                                                       |
| --------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| `The file '<filename>' does not exist.` | The specified file does not exist or the path is incorrect. | Ensure the file exists and check the filename.                 |
| `An error occurred: ...`                | Unknown error during file reading or writing.               | Check file permissions and ensure the input format is correct. |

---

## 📌 **Customization**

- The JSON output file **automatically takes the same name** as the input file but with a `.json` extension.
- If you want a **custom output filename**, modify this line in the script:
  ```python
  output_file = "my_custom_output.json"
  ```

---

## 📌 **Author**

🛠️ This script was developed to **easily convert BIND DNS zone configurations into JSON format for NetBox DNS integration**.


