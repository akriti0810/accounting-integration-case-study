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

The complete generated output is available in [the reconciliation summary](../output/reconciliation_summary.csv).

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

The test suite verifies four core controls:

1. A valid record passes validation.
2. A missing receipt is routed as an exception.
3. A high-value transaction without approval is blocked.
4. The journal balances and the eligible source total reconciles to the export.

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
6. **Next phase:** Validate the workflow in an accounting-system sandbox before any production connection.
