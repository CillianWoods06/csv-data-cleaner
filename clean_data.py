"""
CSV Data Cleaner
----------------
Takes a messy CSV of appointment records and produces a clean version
plus a short quality report. Uses only the Python standard library.

Usage:
    python clean_data.py messy_appointments.csv clean_appointments.csv
"""

import csv
import sys
from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y"]
VALID_STATUSES = {"attended", "cancelled", "no-show"}


def parse_date(text):
    """Try several common date formats and return an ISO date string, or None."""
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def clean_row(row):
    """Return a cleaned copy of one row, or None if the row is unusable."""
    name = " ".join(row["patient_name"].split()).title()
    date = parse_date(row["date"])
    clinic = row["clinic"].strip().title()
    status = row["status"].strip().lower().replace(" ", "-")

    if not name or date is None:
        return None
    if status not in VALID_STATUSES:
        status = "unknown"

    return {
        "appointment_id": row["appointment_id"].strip(),
        "patient_name": name,
        "date": date,
        "clinic": clinic,
        "status": status,
    }


def main(in_path, out_path):
    seen_ids = set()
    cleaned, dropped, duplicates = [], 0, 0

    with open(in_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            result = clean_row(row)
            if result is None:
                dropped += 1
                continue
            if result["appointment_id"] in seen_ids:
                duplicates += 1
                continue
            seen_ids.add(result["appointment_id"])
            cleaned.append(result)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned[0].keys())
        writer.writeheader()
        writer.writerows(cleaned)

    print("Data quality report")
    print("-------------------")
    print(f"Clean rows written: {len(cleaned)}")
    print(f"Rows dropped (missing name or bad date): {dropped}")
    print(f"Duplicate IDs removed: {duplicates}")
    print(f"Rows with unknown status: {sum(r['status'] == 'unknown' for r in cleaned)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_data.py <input.csv> <output.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
