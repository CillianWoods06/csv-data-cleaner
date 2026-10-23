"""Unit tests for the cleaning functions. Run with: python -m unittest"""

import unittest

from cleaner.cleaning import clean_name, clean_records, clean_status, parse_date, parse_fee
from cleaner.report import clinic_summary


class TestFields(unittest.TestCase):

    def test_clean_name(self):
        self.assertEqual(clean_name("  mary   o'brien "), "Mary O'Brien")
        self.assertEqual(clean_name(""), "")

    def test_parse_date_formats(self):
        for text in ["2026-01-15", "15/01/2026", "15-01-2026", "15 Jan 2026"]:
            self.assertEqual(parse_date(text), "2026-01-15")

    def test_parse_date_rejects_bad_dates(self):
        self.assertIsNone(parse_date("not a date"))
        self.assertIsNone(parse_date("31/02/2026"))  # 31 February doesn't exist

    def test_clean_status(self):
        self.assertEqual(clean_status("No Show"), "no-show")
        self.assertEqual(clean_status("NO-SHOW"), "no-show")
        self.assertEqual(clean_status("ATTENDED"), "attended")
        self.assertEqual(clean_status("rescheduled"), "unknown")

    def test_parse_fee(self):
        self.assertEqual(parse_fee("€60"), 60.0)
        self.assertEqual(parse_fee("45.00"), 45.0)
        self.assertIsNone(parse_fee("sixty"))
        self.assertIsNone(parse_fee(""))


class TestRecords(unittest.TestCase):

    def row(self, appt_id, name="Test Person", date="2026-01-15", status="attended"):
        return {"appointment_id": appt_id, "patient_name": name, "date": date,
                "clinic": "salthill", "status": status, "fee": "60"}

    def test_duplicates_and_rejections(self):
        rows = [self.row("A1"), self.row("A1"), self.row("A2", name=""), self.row("A3", date="bad")]
        cleaned, rejected = clean_records(rows)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(rejected, [("A1", "duplicate ID"), ("A2", "missing name"), ("A3", "invalid date")])

    def test_clinic_summary(self):
        rows, _ = clean_records([self.row("A1"), self.row("A2", status="no-show")])
        s = clinic_summary(rows)["Salthill"]
        self.assertEqual(s["total"], 2)
        self.assertEqual(s["no_show_rate"], 50.0)
        self.assertEqual(s["revenue"], 60.0)


if __name__ == "__main__":
    unittest.main()
