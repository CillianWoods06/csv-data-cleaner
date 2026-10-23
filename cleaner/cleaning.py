"""
Functions that clean individual fields and whole rows.

Each function does one job, so it can be tested on its own.
"""

from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %b %Y"]
VALID_STATUSES = {"attended", "cancelled", "no-show"}


def clean_name(text):
    """Collapse extra spaces and use title case: '  mary  o'brien ' -> "Mary O'Brien"."""
    return " ".join(text.split()).title()


def parse_date(text):
    """Return the date as YYYY-MM-DD, or None if it is not a real date in a known format."""
    text = text.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def clean_status(text):
    """Standardise status values. 'No Show', 'no show' and 'NO-SHOW' all become 'no-show'."""
    status = "-".join(text.strip().lower().replace("-", " ").split())
    return status if status in VALID_STATUSES else "unknown"


def parse_fee(text):
    """Turn '€60', '45.00' or '60' into a float. Returns None if it isn't a number."""
    cleaned = text.strip().replace("€", "")
    try:
        return round(float(cleaned), 2)
    except ValueError:
        return None


def clean_row(row):
    """
    Clean one row.

    Returns (clean_row, None) if the row is usable,
    or (None, reason) if it has to be rejected.
    """
    name = clean_name(row["patient_name"])
    if not name:
        return None, "missing name"

    date = parse_date(row["date"])
    if date is None:
        return None, "invalid date"

    return {
        "appointment_id": row["appointment_id"].strip(),
        "patient_name": name,
        "date": date,
        "clinic": clean_name(row["clinic"]),
        "status": clean_status(row["status"]),
        "fee": parse_fee(row.get("fee", "")),
    }, None


def clean_records(rows):
    """
    Clean a list of rows and remove duplicate appointment IDs.

    Returns (cleaned_rows, rejected) where rejected is a list of
    (appointment_id, reason) pairs, so problems can be followed up.
    """
    cleaned, rejected, seen = [], [], set()

    for row in rows:
        result, reason = clean_row(row)
        if result is None:
            rejected.append((row["appointment_id"].strip(), reason))
        elif result["appointment_id"] in seen:
            rejected.append((result["appointment_id"], "duplicate ID"))
        else:
            seen.add(result["appointment_id"])
            cleaned.append(result)

    return cleaned, rejected
