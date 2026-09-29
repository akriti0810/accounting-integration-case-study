# Corporate Card Accounting Automation — Independent Case Study

> **Independent portfolio case study.** All organizations, people, vendors, transactions, and amounts are fictional. The project explores how corporate-card activity can be validated, mapped, and prepared for accounting using sample data.

## Business problem

AK Labs, a fictional 75-person software company, needs a reliable process for transferring corporate-card transactions into its accounting system. This solution translates business requirements into GL, department, and entity mappings; validates transaction readiness; routes exceptions; and reconciles export totals before posting.

## Results snapshot

| Result | Evidence |
|---|---:|
| Fictional source transactions evaluated | 20 |
| Source activity evaluated | $9,540.09 |
| Eligible activity prepared for export | $6,854.06 |
| Exceptions routed for correction | 8 records / $2,686.03 |
| Journal output | 24 balanced debit/credit lines |
| Journal balance difference | $0.00 |
| Source-to-export difference | $0.00 |
| Automated controls tested | 4 passing tests |

See the linked [results snapshot](docs/results_snapshot.md), [exception queue](output/exceptions.csv), [journal export](output/ready_for_export.csv), and [reconciliation summary](output/reconciliation_summary.csv).

## Design goals

1. Apply consistent accounting mappings and validation rules.
2. Prevent incomplete or duplicate records from reaching the export.
3. Give Finance an actionable exception queue with owners and next steps.
4. Reconcile eligible source activity to a balanced journal export.

## Repository guide

| Area | What it demonstrates |
|---|---|
| [Configuration](config) | Requirements translated into product configuration |
| [Sample transactions](data/sample_transactions.csv) | Fictional corporate-card activity with valid and invalid cases |
| [Validation workflow](src/validate_transactions.py) | Mapping, validation, exception routing, and reconciliation |
| [Automated tests](tests/test_validation.py) | Automated control tests |
| [Results snapshot](docs/results_snapshot.md) | Review-ready examples of generated outputs and control results |

Supporting documentation in [docs/](docs) covers assumptions and requirements, test scenarios, operating guidance, and a go-live checklist.

## Workflow

```text
Card transactions → validation and mapping → ready records + exception queue
                  → balanced journal export → Finance reconciliation and approval
```

## Validation and accounting controls

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

## Suggested demo flow

Start with the business problem and acceptance criteria, show how requirements become mappings, run the validator, trace one exception from diagnosis to resolution, and finish with the reconciliation and go-live controls. A concise walkthrough is included in [the results snapshot](docs/results_snapshot.md#two-minute-project-walkthrough).
