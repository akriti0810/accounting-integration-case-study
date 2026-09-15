# User Acceptance Test Plan

| ID | Scenario | Expected result | Priority |
|---|---|---|---|
| T01 | Fully coded and approved record | Two balanced journal lines export | High |
| T02 | Missing receipt or memo | Blocked and assigned to Cardholder | High |
| T03 | Unmapped vendor | Blocked and assigned to Finance | High |
| T04 | Invalid department or entity | Blocked and assigned to Finance | High |
| T05 | More than $1,000 without approval | Blocked and assigned to Manager | High |
| T06 | Duplicate transaction ID | Every occurrence blocked for review | High |
| T07 | More than $1,000 with approval | Exported | Medium |
| T08 | Journal created | Total debits equal total credits | High |
| T09 | Reconciliation created | Eligible source total equals export debit total | High |

## Entry criteria

- Finance approved accounts, departments, entities, and threshold.
- Test data includes successful and failing scenarios.
- Exception ownership is agreed.

## Exit criteria

- All high-priority tests pass.
- No journal imbalance remains.
- Finance signs off on mappings, sample output, and reconciliation.
- Operating guide and launch ownership are confirmed.

Defects should record the transaction ID, expected and actual behavior, severity, owner, and resolution. Escalations should include reproduction steps and sample records.
