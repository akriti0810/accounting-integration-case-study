# Corporate Card → Accounting Integration Case Study

> **Portfolio simulation — not a production deployment.** All organizations, people, vendors, transactions, and amounts are fictional. This project demonstrates an implementation approach; it does not represent professional Brex, QuickBooks, or NetSuite configuration experience.

## Executive summary

Northstar Labs, a fictional 75-person software company, needs a reliable process for transferring corporate-card transactions into its accounting system. This solution translates business requirements into GL, department, and entity mappings; validates transaction readiness; routes exceptions; and reconciles export totals before posting.

## Customer outcomes

1. Apply consistent accounting mappings and validation rules.
2. Prevent incomplete or duplicate records from reaching the export.
3. Give Finance an actionable exception queue with owners and next steps.
4. Reconcile eligible source activity to a balanced journal export.

## Repository guide

| Area | What it demonstrates |
|---|---|
| [Requirements](docs/requirements.md) | Discovery, scope, stakeholders, and acceptance criteria |
| [Configuration](config) | Requirements translated into product configuration |
| [Sample transactions](data/sample_transactions.csv) | Fictional card-transaction dataset |
| [Validation workflow](src/validate_transactions.py) | Validation, mapping, exception, and reconciliation workflow |
| [Automated tests](tests/test_validation.py) | Automated control tests |
| [Test plan](docs/test_plan.md) | User-acceptance test scenarios |
| [Customer guide](docs/customer_guide.md) | Plain-language operating guide |
| [Go-live checklist](docs/go_live_checklist.md) | Launch readiness and escalation |

## Workflow

```text
Card transactions → validation and mapping → ready records + exception queue
                  → balanced journal export → Finance reconciliation and approval
```

## Controls

- Required receipt, memo, entity, department, and vendor checks
- Vendor-to-GL and entity mapping validation
- Duplicate transaction-ID detection
- Approval required above the configured $1,000 threshold
- Balanced debit and credit journal lines
- Source-to-export reconciliation with documented exclusions

## Run locally

Requires Python 3.9+ and only the standard library.

```bash
python3 src/validate_transactions.py
python3 -m unittest discover -s tests -v
```

Generated files appear in `output/`: `ready_for_export.csv`, `exceptions.csv`, and `reconciliation_summary.csv`.

## Limitations

- CSV journal import represents the accounting system; there is no live API connection.
- Tax, foreign exchange, refunds, and split allocations are out of scope.
- Production use would require customer-approved mappings, sandbox testing, secure authentication, access controls, and audit logging.

## Interview walkthrough

Explain the customer problem and acceptance criteria, show how requirements become mappings, run the validator, trace one exception from diagnosis to resolution, and finish with reconciliation and go-live controls.
