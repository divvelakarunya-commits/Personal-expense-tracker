"""Basic tests. Run with:  python -m unittest"""

import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import expense_tracker as et


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        et.DB_FILE = Path(self.tmp.name) / "test.db"

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, func, **kwargs):
        buf = StringIO()
        with redirect_stdout(buf):
            func(Namespace(**kwargs))
        return buf.getvalue()

    def add(self, amount, category, desc="", day="2026-11-01"):
        return self.run_cmd(et.add_expense, amount=amount, category=category,
                            description=desc, date=day)

    def test_add_and_list(self):
        self.add(100.0, "food", "lunch")
        out = self.run_cmd(et.list_expenses, category=None, month=None)
        self.assertIn("Food", out)
        self.assertIn("100.00", out)

    def test_summary_totals(self):
        self.add(100.0, "food")
        self.add(50.0, "food")
        self.add(200.0, "travel")
        out = self.run_cmd(et.summary, month="2026-11")
        self.assertIn("350.00", out)

    def test_delete(self):
        self.add(10.0, "misc")
        out = self.run_cmd(et.delete_expense, id=1)
        self.assertIn("Deleted", out)

    def test_validators(self):
        self.assertEqual(et.positive_amount("12.345"), 12.35)
        with self.assertRaises(Exception):
            et.positive_amount("-5")
        with self.assertRaises(Exception):
            et.valid_date("11/11/2026")


if __name__ == "__main__":
    unittest.main()
