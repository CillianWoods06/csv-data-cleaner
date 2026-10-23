# CSV Data Cleaner

A small Python script that turns a messy CSV export into clean, consistent data and prints a short data-quality report.

## What it fixes
- Extra spaces and inconsistent capitalisation in names and clinic names
- Dates in four different formats, converted to `YYYY-MM-DD`
- Status values standardised (`attended`, `cancelled`, `no-show`), anything else marked `unknown`
- Rows with a missing name or an unreadable date are dropped
- Duplicate appointment IDs are removed

## Run it
```bash
python clean_data.py messy_appointments.csv clean_appointments.csv
```

## Example output
```
Data quality report
-------------------
Clean rows written: 5
Rows dropped (missing name or bad date): 2
Duplicate IDs removed: 1
Rows with unknown status: 1
```

## Skills shown
Python, file handling, data validation, data cleaning — the same steps I'd do in Power Query, written in code.

*All data is fictional.*
