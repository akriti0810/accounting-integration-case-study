# Results Snapshot

This page provides a quick review of the generated outputs from the fictional AK Labs case study. All organizations, people, transactions, vendors, and amounts are simulated.

## Reconciliation summary

| Metric | Result |
|---|---:|
| Source transactions | 20 |
| Source total | $9,540.09 |
| Eligible source total | $6,854.06 |
| Exception transaction total | $2,686.03 |
| Export debit total | $6,854.06 |
| Export credit total | $6,854.06 |
| Journal balance difference | $0.00 |
| Source-to-export difference | $0.00 |
| QuickBooks sandbox journal entries created and read back | 12 |
| QuickBooks sandbox journal lines verified | 24 |
| QuickBooks sandbox debit total | $6,854.06 |
| QuickBooks sandbox credit total | $6,854.06 |
| QuickBooks sandbox-to-source difference | $0.00 |

The complete generated output is available in [the source reconciliation](../output/reconciliation_summary.csv) and [QuickBooks sandbox reconciliation](../output/quickbooks_sandbox_reconciliation.csv).

## QuickBooks Online sandbox verification

The connector used OAuth 2.0 to connect to a QuickBooks Online developer sandbox, created or reused the configured AK Labs chart-of-accounts records, posted one balanced journal entry for each eligible source transaction, and retrieved every entry from QuickBooks for verification. The read-back reconciled 24 journal lines and $6,854.06 in both debits and credits to the eligible source activity with a $0.00 difference.

This is an independent implementation using a fictional sandbox company, not professional client deployment experience.

## Exception queue sample

| Transaction | Issue | Owner | Corrective action |
|---|---|---|---|
| TXN-1005 | Missing receipt | Cardholder | Attach a valid receipt |
| TXN-1012 | Unmapped vendor | Finance | Approve a GL mapping or correct the vendor |
| TXN-1013 | Missing approval | Manager | Review and record approval |
| TXN-1019 | Duplicate ID | Finance | Investigate source duplication |

The full queue contains eight exception records across receipt, memo, mapping, approval, and duplicate controls: [view the exception queue](../output/exceptions.csv).

## Journal-entry sample

| Transaction | Account | Department | Debit | Credit |
|---|---|---|---:|---:|
| TXN-1001 | 6100 — Cloud Infrastructure | Engineering | $842.19 | $0.00 |
| TXN-1001 | 2100 — Corporate Card Payable | Engineering | $0.00 | $842.19 |
| TXN-1002 | 6200 — Software Subscriptions | Design | $180.00 | $0.00 |
| TXN-1002 | 2100 — Corporate Card Payable | Design | $0.00 | $180.00 |

The full generated journal contains 24 lines for 12 eligible transactions: [view the journal export](../output/ready_for_export.csv).

## Automated checks

The test suite verifies eight controls across the validation workflow and QuickBooks connector, including:

1. A valid record passes validation.
2. A missing receipt is routed as an exception.
3. A high-value transaction without approval is blocked.
4. The journal balances and the eligible source total reconciles to the export.
5. One balanced QuickBooks payload is created per eligible transaction.
6. QuickBooks payload totals reconcile to $6,854.06.
7. Missing account mappings are blocked.
8. Retrieved QuickBooks journals are summarized and balanced correctly.

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Two-minute project walkthrough

1. **Problem:** AK Labs needs a repeatable process for preparing corporate-card activity for accounting.
2. **Configuration:** Vendor, entity, department, and approval requirements are stored as editable mappings and rules.
3. **Processing:** The Python workflow validates each transaction, separates ready records from exceptions, and creates balanced journal lines.
4. **Exception handling:** Each issue is assigned an owner and corrective action instead of being silently dropped.
5. **Reconciliation:** Eligible source activity ties to the journal export with a $0.00 difference.
6. **QuickBooks verification:** Post 12 journals to a developer sandbox, retrieve all 24 lines, and reconcile the read-back to source activity with a $0.00 difference.
