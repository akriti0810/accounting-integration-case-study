"""Create validated accounting-import artifacts from fictional card data."""

import csv
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output"
THRESHOLD = Decimal("1000.00")


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def configuration():
    vendors = {r["vendor"]: r for r in read_csv(ROOT / "config/vendor_gl_mapping.csv")}
    entities = {r["card_entity"]: r for r in read_csv(ROOT / "config/entities.csv")}
    departments = {r["department"] for r in read_csv(ROOT / "config/departments.csv") if r["status"] == "Active"}
    return vendors, entities, departments


def validate(row, duplicates, vendors, entities, departments):
    issues = []
    if row["transaction_id"] in duplicates:
        issues.append(("DUPLICATE_ID", "Finance", "Investigate source duplication"))
    if row["receipt_attached"].lower() != "yes":
        issues.append(("MISSING_RECEIPT", "Cardholder", "Attach a valid receipt"))
    if not row["memo"].strip():
        issues.append(("MISSING_MEMO", "Cardholder", "Add the business purpose"))
    if row["vendor"] not in vendors:
        issues.append(("UNMAPPED_VENDOR", "Finance", "Approve a GL mapping or correct vendor"))
    if row["department"] not in departments:
        issues.append(("INVALID_DEPARTMENT", "Finance", "Select an approved department"))
    if row["entity"] not in entities:
        issues.append(("INVALID_ENTITY", "Finance", "Select an approved entity"))
    if Decimal(row["amount"]) > THRESHOLD and row["approved"].lower() != "yes":
        issues.append(("MISSING_APPROVAL", "Manager", "Review and record approval"))
    return issues


def process():
    rows = read_csv(ROOT / "data/sample_transactions.csv")
    vendors, entities, departments = configuration()
    counts = Counter(r["transaction_id"] for r in rows)
    duplicates = {key for key, count in counts.items() if count > 1}
    journal, exceptions = [], []
    eligible_total = Decimal("0")

    for row in rows:
        issues = validate(row, duplicates, vendors, entities, departments)
        if issues:
            for code, owner, action in issues:
                exceptions.append({"transaction_id": row["transaction_id"], "vendor": row["vendor"],
                                   "amount": row["amount"], "issue_code": code,
                                   "owner": owner, "recommended_action": action})
            continue
        amount = Decimal(row["amount"])
        eligible_total += amount
        vendor, entity = vendors[row["vendor"]], entities[row["entity"]]
        base = {"transaction_id": row["transaction_id"], "date": row["date"],
                "accounting_entity": entity["accounting_entity"],
                "department": row["department"], "description": row["memo"]}
        journal += [
            {**base, "account": vendor["gl_account"], "account_name": vendor["gl_account_name"],
             "debit": f"{amount:.2f}", "credit": "0.00"},
            {**base, "account": entity["cash_account"], "account_name": "Corporate Card Payable",
             "debit": "0.00", "credit": f"{amount:.2f}"},
        ]

    source_total = sum((Decimal(r["amount"]) for r in rows), Decimal("0"))
    debit = sum((Decimal(r["debit"]) for r in journal), Decimal("0"))
    credit = sum((Decimal(r["credit"]) for r in journal), Decimal("0"))
    reconciliation = [
        {"metric": "Source transaction count", "value": str(len(rows))},
        {"metric": "Source total", "value": f"{source_total:.2f}"},
        {"metric": "Eligible source total", "value": f"{eligible_total:.2f}"},
        {"metric": "Exception transaction total", "value": f"{source_total - eligible_total:.2f}"},
        {"metric": "Export debit total", "value": f"{debit:.2f}"},
        {"metric": "Export credit total", "value": f"{credit:.2f}"},
        {"metric": "Journal balance difference", "value": f"{debit - credit:.2f}"},
        {"metric": "Source-to-export difference", "value": f"{eligible_total - debit:.2f}"},
    ]
    return journal, exceptions, reconciliation


def main():
    journal, exceptions, reconciliation = process()
    write_csv(OUTPUT / "ready_for_export.csv", journal,
              ["transaction_id", "date", "accounting_entity", "account", "account_name",
               "department", "description", "debit", "credit"])
    write_csv(OUTPUT / "exceptions.csv", exceptions,
              ["transaction_id", "vendor", "amount", "issue_code", "owner", "recommended_action"])
    write_csv(OUTPUT / "reconciliation_summary.csv", reconciliation, ["metric", "value"])
    print(f"Created {len(journal)} journal lines and {len(exceptions)} exception records.")


if __name__ == "__main__":
    main()
