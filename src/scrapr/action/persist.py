import json
import csv
from typing import List, Dict


def write_to_json(data: List[Dict[str, str]], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been written to {filename} in JSON format.")


def write_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    if not data:
        print("The data list is empty. No CSV file will be created.")
        return

    fieldnames = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in data:
            writer.writerow(row)

    print(f"Data has been written to {filename} in CSV format.")
