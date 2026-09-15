import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from validate_transactions import configuration, process, validate  # noqa: E402


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.vendors, self.entities, self.departments = configuration()
        self.row = {"transaction_id": "TEST-1", "date": "2026-08-01", "employee": "Test User",
                    "vendor": "AWS", "amount": "100.00", "currency": "USD",
                    "department": "Engineering", "entity": "Northstar Labs US",
                    "receipt_attached": "yes", "memo": "Cloud usage", "approved": "yes"}

    def test_valid_record(self):
        self.assertEqual(validate(self.row, set(), self.vendors, self.entities, self.departments), [])

    def test_missing_receipt(self):
        self.row["receipt_attached"] = "no"
        issues = validate(self.row, set(), self.vendors, self.entities, self.departments)
        self.assertTrue(any(issue[0] == "MISSING_RECEIPT" for issue in issues))

    def test_unapproved_high_value(self):
        self.row.update(amount="1000.01", approved="no")
        issues = validate(self.row, set(), self.vendors, self.entities, self.departments)
        self.assertTrue(any(issue[0] == "MISSING_APPROVAL" for issue in issues))

    def test_export_balances_and_reconciles(self):
        journal, _, reconciliation = process()
        self.assertEqual(sum(Decimal(r["debit"]) for r in journal),
                         sum(Decimal(r["credit"]) for r in journal))
        metrics = {r["metric"]: r["value"] for r in reconciliation}
        self.assertEqual(metrics["Journal balance difference"], "0.00")
        self.assertEqual(metrics["Source-to-export difference"], "0.00")


if __name__ == "__main__":
    unittest.main()
