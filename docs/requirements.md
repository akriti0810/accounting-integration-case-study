# Customer Requirements and Solution Design

## Customer profile

Northstar Labs is a fictional 75-person software company with US and UK entities. Finance currently reviews corporate-card activity in spreadsheets before importing journals into its accounting system.

## Discovery questions

- Who owns policy, accounting mappings, exceptions, and final posting?
- What is the monthly-close deadline, and where do errors occur today?
- Which chart-of-accounts, entities, departments, and cash accounts are valid?
- Which fields and approvals are mandatory before export?
- How should refunds, foreign currency, and split allocations be handled?
- Is the target a native integration, API connection, or file import?
- What are the test, access, failure-notification, and rollback expectations?

## Simulation requirements

| ID | Requirement | Control |
|---|---|---|
| R1 | Every transaction has a unique ID | Duplicate-ID validation |
| R2 | Receipt and business-purpose memo are required | Required-field validation |
| R3 | Vendor, department, and entity use approved values | Configuration tables |
| R4 | Transactions above $1,000 require approval | Threshold rule |
| R5 | Finance receives actionable exceptions | Reason, owner, and next action |
| R6 | Eligible records reconcile to a balanced export | Debit/credit and control totals |

## Scope

**In scope:** mappings, validation, balanced journal CSV, exception queue, reconciliation, testing, customer guide, and go-live planning.

**Out of scope:** live credentials or APIs, production security, tax, foreign exchange, refunds, and split allocations.

## Acceptance criteria

- Every exported transaction has valid mappings and required documentation.
- No duplicated transaction ID is exported.
- Debit and credit totals balance to the cent.
- Every excluded record has an owner and corrective action.
- Finance can reproduce and approve reconciliation before posting.

## Roles

| Stakeholder | Responsibility |
|---|---|
| Finance lead | Approves mappings, policy, and reconciliation |
| Implementation consultant | Discovery, configuration, testing, and launch coordination |
| Cardholder/manager | Documentation and approvals |
| Accounting administrator | Imports the approved journal and confirms posting |

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Incorrect GL mapping | Finance sign-off and sample testing |
| Incomplete records exported | Blocking validation controls |
| Duplicate posting | Unique-ID validation |
| Unbalanced journal | Debit/credit control total |
| Delayed close | Named owners and escalation path |
