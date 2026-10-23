# Appointment Data Cleaner

A Python tool that takes a messy appointments export, cleans it, explains what it rejected and why, and produces a short business summary per clinic.

I built this to practise doing in code what I usually do in **Power Query**: fixing inconsistent text, standardising dates, removing duplicates and flagging bad data. Doing it in Python makes every step repeatable and testable.

## The problem
Exports from booking systems are rarely clean. The sample file (`data/messy_appointments.csv`, fictional data) has:

| Issue | Example |
|---|---|
| Inconsistent capitalisation and spacing | `  mary   o'brien `, `GALWAY CENTRAL` |
| Four different date formats | `2026-01-14`, `15/01/2026`, `16-01-2026`, `20 Jan 2026` |
| Impossible dates | `31/02/2026` |
| Inconsistent status values | `No Show`, `no show`, `No-Show`, `rescheduled` |
| Messy fees | `€60`, `45.00`, `sixty`, blank |
| Missing names and duplicate IDs | |

## What it produces
- `output/clean_appointments.csv`: clean data, ready to load into Excel or Power BI
- `output/report.md`: a data-quality summary (what was rejected and why) and a per-clinic breakdown of no-show rate and revenue. See [docs/sample_report.md](docs/sample_report.md).

## Design decisions
- **Reject vs. flag.** A row with no name or an invalid date can't be used, so it's rejected and logged with a reason. A row with an unknown status or a missing fee is still useful, so it's kept and flagged instead.
- **Small, single-purpose functions.** Each field has its own cleaning function, which makes them easy to unit test.
- **No external libraries.** It only uses the Python standard library, so it runs anywhere without installing anything.

## Project structure
```
cleaner/
  cleaning.py   field and row cleaning rules
  report.py     per-clinic summary and Markdown report
tests/
  test_cleaning.py
data/
  messy_appointments.csv
main.py         command-line entry point
```

## How to run
```bash
python main.py data/messy_appointments.csv --out output
python -m unittest        # 7 tests
```

## What I'd add next
- Load the data with pandas for larger files
- Save rejected rows to their own CSV so someone can fix them at the source
- Connect the clean output to a Power BI dashboard
