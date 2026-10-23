"""Builds a summary of the cleaned data and writes it as a Markdown report."""

from collections import defaultdict


def clinic_summary(rows):
    """
    Per-clinic totals: appointments, attended, no-shows, no-show rate and revenue.
    Revenue only counts attended appointments with a known fee.
    """
    stats = defaultdict(lambda: {"total": 0, "attended": 0, "no_show": 0, "revenue": 0.0})

    for row in rows:
        s = stats[row["clinic"]]
        s["total"] += 1
        if row["status"] == "attended":
            s["attended"] += 1
            s["revenue"] += row["fee"] or 0
        elif row["status"] == "no-show":
            s["no_show"] += 1

    for s in stats.values():
        s["no_show_rate"] = round(100 * s["no_show"] / s["total"], 1)

    return dict(sorted(stats.items()))


def write_report(path, total_in, cleaned, rejected):
    """Write a short data-quality and business summary that a manager could read."""
    missing_fee = sum(1 for r in cleaned if r["fee"] is None)
    unknown_status = sum(1 for r in cleaned if r["status"] == "unknown")
    summary = clinic_summary(cleaned)

    lines = [
        "# Appointment Data Report",
        "",
        "## Data quality",
        f"- Rows read: {total_in}",
        f"- Clean rows kept: {len(cleaned)}",
        f"- Rows rejected: {len(rejected)}",
        f"- Rows with unknown status: {unknown_status}",
        f"- Rows with missing or invalid fee: {missing_fee}",
        "",
        "### Rejected rows",
        "| Appointment | Reason |",
        "|---|---|",
    ]
    lines += [f"| {appt} | {reason} |" for appt, reason in rejected]

    lines += [
        "",
        "## By clinic",
        "| Clinic | Appointments | Attended | No-shows | No-show rate | Revenue |",
        "|---|---|---|---|---|---|",
    ]
    for clinic, s in summary.items():
        lines.append(
            f"| {clinic} | {s['total']} | {s['attended']} | {s['no_show']} "
            f"| {s['no_show_rate']}% | €{s['revenue']:.2f} |"
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
