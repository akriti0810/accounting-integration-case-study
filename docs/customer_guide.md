# Finance User Guide

1. Confirm all mapping files contain Finance-approved values.
2. Export card activity using the columns in `data/sample_transactions.csv`.
3. Run `python3 src/validate_transactions.py`.
4. Review `output/exceptions.csv` before the journal export.
5. Route missing documentation to the cardholder, approval gaps to the manager, and mapping issues to Finance.
6. Correct source data or approved configuration; do not edit the generated journal to bypass controls.
7. Rerun and review `output/reconciliation_summary.csv`.
8. Import `output/ready_for_export.csv` only after Finance approval.

## Escalate when

- Debit and credit totals do not balance.
- A configuration change affects previously tested results.
- A repeatable failure remains after the source data is corrected.
- A new GL account, department, or entity is required.

Include transaction IDs, expected behavior, actual behavior, and reproduction steps in an escalation.
