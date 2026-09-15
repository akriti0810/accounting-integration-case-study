# Corporate Card Accounting Automation — Independent Case Study

> **Independent portfolio case study.** All organizations, people, vendors, transactions, and amounts are fictional. The project explores how corporate-card activity can be validated, mapped, and prepared for accounting using sample data.

## Overview

AK Labs, a fictional 75-person software company, needs a reliable process for transferring corporate-card transactions into its accounting system. The workflow maps accounting dimensions, checks transaction readiness, routes exceptions, and reconciles eligible activity before export.

## Design goals

1. Apply consistent accounting mappings and validation rules.
2. Prevent incomplete or duplicate records from reaching the export.
3. Give Finance an actionable exception queue with owners and next steps.
4. Reconcile eligible source activity to a balanced journal export.

## Core artifacts

| Area | Purpose |
|---|---|
| [Configuration](config) | Vendor-to-GL, entity, and department mappings |
| [Sample transactions](data/sample_transactions.csv) | Fictional corporate-card activity with valid and invalid cases |
| [Validation workflow](src/validate_transactions.py) | Mapping, validation, exception routing, and reconciliation |
| [Automated tests](tests/test_validation.py) | Checks for core controls and balanced outputs |
| [Generated outputs](output) | Journal export, exception queue, and reconciliation summary |

Supporting documentation in [docs/](docs) covers assumptions and requirements, test scenarios, operating guidance, and a go-live checklist.

## Workflow

```text
Card transactions → validation and mapping → ready records + exception queue
                  → balanced journal export → Finance reconciliation and approval
```

## Validation controls

- Required receipt and business-purpose memo
- Approved vendor, department, and entity mappings
- Duplicate transaction-ID detection
- Manager approval above the configured $1,000 threshold
- Balanced debit and credit journal lines
- Eligible-source-to-export reconciliation

## Run locally

Requires Python 3.9+ and only the standard library.

```bash
python3 src/validate_transactions.py
python3 -m unittest discover -s tests -v
```

The workflow writes `ready_for_export.csv`, `exceptions.csv`, and `reconciliation_summary.csv` to the [output](output) folder.

## Scope

This version uses a CSV journal export rather than a live accounting-system connection. Tax, foreign exchange, refunds, and split allocations are outside the current scope.
