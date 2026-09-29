import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from quickbooks_sandbox import build_journal_payload, grouped_journal_lines, summarize_posted_journals  # noqa: E402


class QuickBooksSandboxTests(unittest.TestCase):
    def setUp(self):
        self.grouped = grouped_journal_lines()
        self.account_ids = {"2100": "2", "6100": "6", "6200": "7", "6300": "8",
                            "6500": "9", "6600": "10", "6700": "11"}

    def test_builds_one_balanced_payload_per_transaction(self):
        payloads = [build_journal_payload(key, value, self.account_ids)
                    for key, value in self.grouped.items()]
        self.assertEqual(len(payloads), 12)
        self.assertTrue(all(len(payload["Line"]) == 2 for payload in payloads))

    def test_payload_total_matches_eligible_activity(self):
        debit = Decimal("0")
        credit = Decimal("0")
        for key, value in self.grouped.items():
            payload = build_journal_payload(key, value, self.account_ids)
            for line in payload["Line"]:
                amount = Decimal(str(line["Amount"]))
                if line["JournalEntryLineDetail"]["PostingType"] == "Debit":
                    debit += amount
                else:
                    credit += amount
        self.assertEqual(debit, Decimal("6854.06"))
        self.assertEqual(credit, Decimal("6854.06"))

    def test_rejects_missing_account_mapping(self):
        key, lines = next(iter(self.grouped.items()))
        with self.assertRaisesRegex(ValueError, "Missing QuickBooks account ID"):
            build_journal_payload(key, lines, {})

    def test_summarizes_read_back_journals(self):
        journal = {"Line": [
            {"Amount": 25.5, "JournalEntryLineDetail": {"PostingType": "Debit"}},
            {"Amount": 25.5, "JournalEntryLineDetail": {"PostingType": "Credit"}},
        ]}
        self.assertEqual(summarize_posted_journals([journal]), (Decimal("25.5"), Decimal("25.5")))
