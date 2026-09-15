# Corporate Card → Accounting Integration Case Study


> **Portfolio simulation.** All organizations, people, vendors, transactions, and amounts are fictional. This project demonstrates a corporate-card-to-accounting implementation workflow using sample data.


## Executive summary


AK Labs, a fictional 75-person software company, needs a reliable process for transferring corporate-card transactions into its accounting system. This solution translates business requirements into GL, department, and entity mappings; validates transaction readiness; routes exceptions; and reconciles export totals before posting.


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
