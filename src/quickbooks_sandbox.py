"""Prepare and optionally post validated journals to a QuickBooks Online sandbox.

The default mode is a credential-free preview. Live sandbox mode requires the
QBO_ACCESS_TOKEN and QBO_REALM_ID environment variables. Secrets are never
written to disk.
"""

import argparse
import csv
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SANDBOX_BASE = "https://sandbox-quickbooks.api.intuit.com"


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def account_configuration():
    return {row["local_account"]: row for row in read_csv(ROOT / "config/quickbooks_accounts.csv")}


def grouped_journal_lines():
    grouped = defaultdict(list)
    for row in read_csv(ROOT / "output/ready_for_export.csv"):
        grouped[row["transaction_id"]].append(row)
    return dict(grouped)


def build_journal_payload(transaction_id, lines, account_ids):
    if not lines:
        raise ValueError("A journal entry requires at least one line")
    payload_lines = []
    debit_total = Decimal("0")
    credit_total = Decimal("0")
    for line in lines:
        account = line["account"]
        if account not in account_ids:
            raise ValueError(f"Missing QuickBooks account ID for local account {account}")
        debit, credit = Decimal(line["debit"]), Decimal(line["credit"])
        if debit > 0:
            posting_type, amount = "Debit", debit
            debit_total += debit
        elif credit > 0:
            posting_type, amount = "Credit", credit
            credit_total += credit
        else:
            raise ValueError(f"Line for {transaction_id} has no debit or credit amount")
        payload_lines.append({
            "DetailType": "JournalEntryLineDetail",
            "Amount": float(amount),
            "Description": f'{line["description"]} | Department: {line["department"]} | Source: {transaction_id}',
            "JournalEntryLineDetail": {
                "PostingType": posting_type,
                "AccountRef": {"value": str(account_ids[account])},
            },
        })
    if debit_total != credit_total:
        raise ValueError(f"Unbalanced journal {transaction_id}: {debit_total} != {credit_total}")
    return {
        "TxnDate": lines[0]["date"],
        "PrivateNote": f"AK Labs sandbox import | {transaction_id}",
        "Line": payload_lines,
    }


class QuickBooksSandbox:
    def __init__(self, access_token, realm_id):
        self.access_token = access_token
        self.realm_id = realm_id

    def request(self, method, path, body=None):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(
            f"{SANDBOX_BASE}/v3/company/{self.realm_id}/{path}",
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"QuickBooks API returned HTTP {exc.code}: {detail}") from exc

    def accounts(self):
        query = urllib.parse.quote("select * from Account maxresults 1000")
        response = self.request("GET", f"query?query={query}")
        return response.get("QueryResponse", {}).get("Account", [])

    def ensure_accounts(self, configuration):
        existing = {account["Name"]: account for account in self.accounts()}
        account_ids, actions = {}, []
        for local_number, row in configuration.items():
            name = row["quickbooks_name"]
            account = existing.get(name)
            if account is None:
                response = self.request("POST", "account", {
                    "Name": name,
                    "AcctNum": local_number,
                    "AccountType": row["account_type"],
                    "Description": f'AK Labs sandbox mapping for {row["local_account_name"]}',
                })
                account = response["Account"]
                actions.append({"account": local_number, "quickbooks_name": name, "action": "created"})
            else:
                actions.append({"account": local_number, "quickbooks_name": name, "action": "reused"})
            account_ids[local_number] = account["Id"]
        return account_ids, actions

    def post_journal(self, payload):
        return self.request("POST", "journalentry", payload)["JournalEntry"]

    def read_journal(self, journal_id):
        return self.request("GET", f"journalentry/{journal_id}")["JournalEntry"]


def summarize_posted_journals(journals):
    debit = Decimal("0")
    credit = Decimal("0")
    for journal in journals:
        for line in journal["Line"]:
            amount = Decimal(str(line["Amount"]))
            posting_type = line["JournalEntryLineDetail"]["PostingType"]
            if posting_type == "Debit":
                debit += amount
            elif posting_type == "Credit":
                credit += amount
    return debit, credit


def write_preview(payloads):
    path = ROOT / "output/quickbooks_payload_preview.json"
    path.write_text(json.dumps(payloads, indent=2), encoding="utf-8")
    return path


def write_live_evidence(journals, account_actions):
    private_path = ROOT / "output/quickbooks_sandbox_private.json"
    private_path.write_text(json.dumps({"accounts": account_actions, "journals": journals}, indent=2), encoding="utf-8")
    debit, credit = summarize_posted_journals(journals)
    summary_path = ROOT / "output/quickbooks_sandbox_reconciliation.csv"
    rows = [
        ("Environment", "QuickBooks Online sandbox"),
        ("Journal entries created and read back", str(len(journals))),
        ("Journal lines verified", str(sum(len(journal["Line"]) for journal in journals))),
        ("Verified debit total", f"{debit:.2f}"),
        ("Verified credit total", f"{credit:.2f}"),
        ("QuickBooks balance difference", f"{debit - credit:.2f}"),
        ("Expected eligible activity", "6854.06"),
        ("Sandbox-to-source difference", f"{debit - Decimal('6854.06'):.2f}"),
    ]
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)
    return private_path, summary_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--post", action="store_true", help="Create and verify journals in a QuickBooks Online sandbox")
    args = parser.parse_args()

    configuration = account_configuration()
    grouped = grouped_journal_lines()
    if not args.post:
        placeholder_ids = {account: f"QBO_ACCOUNT_ID_{account}" for account in configuration}
        payloads = [build_journal_payload(transaction_id, lines, placeholder_ids)
                    for transaction_id, lines in sorted(grouped.items())]
        path = write_preview(payloads)
        print(f"Prepared {len(payloads)} QuickBooks sandbox journal payloads at {path}")
        return

    access_token = os.environ.get("QBO_ACCESS_TOKEN")
    realm_id = os.environ.get("QBO_REALM_ID")
    if not access_token or not realm_id:
        raise SystemExit("Set QBO_ACCESS_TOKEN and QBO_REALM_ID before using --post")

    client = QuickBooksSandbox(access_token, realm_id)
    account_ids, account_actions = client.ensure_accounts(configuration)
    posted = []
    for transaction_id, lines in sorted(grouped.items()):
        created = client.post_journal(build_journal_payload(transaction_id, lines, account_ids))
        posted.append(client.read_journal(created["Id"]))
    private_path, summary_path = write_live_evidence(posted, account_actions)
    debit, credit = summarize_posted_journals(posted)
    if debit != credit or debit != Decimal("6854.06"):
        raise SystemExit(f"Sandbox reconciliation failed: debit={debit}, credit={credit}")
    print(f"Created and verified {len(posted)} sandbox journals totaling {debit:.2f}.")
    print(f"Private response log: {private_path}")
    print(f"Shareable reconciliation: {summary_path}")


if __name__ == "__main__":
    main()
