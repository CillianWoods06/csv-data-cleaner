"""
Command-line entry point.

Example:
    python main.py data/messy_appointments.csv --out output
"""

import argparse
import csv
import os

from cleaner.cleaning import clean_records
from cleaner.report import write_report

FIELDNAMES = ["appointment_id", "patient_name", "date", "clinic", "status", "fee"]


def main():
    parser = argparse.ArgumentParser(description="Clean an appointments CSV and produce a report.")
    parser.add_argument("input", help="path to the messy CSV file")
    parser.add_argument("--out", default="output", help="folder for the results (default: output)")
    args = parser.parse_args()

    with open(args.input, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    cleaned, rejected = clean_records(rows)

    os.makedirs(args.out, exist_ok=True)
    clean_path = os.path.join(args.out, "clean_appointments.csv")
    report_path = os.path.join(args.out, "report.md")

    with open(clean_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(cleaned)

    write_report(report_path, len(rows), cleaned, rejected)

    print(f"{len(cleaned)} clean rows written to {clean_path}")
    print(f"{len(rejected)} rows rejected - see {report_path}")


if __name__ == "__main__":
    main()
