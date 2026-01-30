import json
import csv
import os

def json_to_csv():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, ".tmp/sorted_contacts.json")
    output_file = os.path.join(base_dir, "contacts.csv")

    try:
        # Read JSON data
        with open(input_file, 'r') as f:
            contacts = json.load(f)

        # Prepare CSV data
        csv_data = []
        for contact in contacts:
            name = contact.get("name", "")
            raw_id = contact.get("id", "")
            
            # Format ID: remove anything after @ (including @)
            formatted_id = raw_id.split('@')[0] if raw_id else ""
            
            csv_data.append({"Name": name, "Phone": formatted_id})

        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Name", "Phone"])
            writer.writeheader()
            writer.writerows(csv_data)

        print(f"Successfully converted {len(csv_data)} contacts to {output_file}")

    except Exception as e:
        print(f"Error converting contacts: {e}")

if __name__ == "__main__":
    json_to_csv()
