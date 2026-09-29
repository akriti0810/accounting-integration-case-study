# QuickBooks Online Sandbox Runbook

## Purpose

Verify that the validated AK Labs journal output can be configured, posted, retrieved, and reconciled in a QuickBooks Online developer sandbox. This is an independent sandbox implementation, not professional client deployment experience.

## Before authorization

1. Run `python3 src/validate_transactions.py`.
2. Run `python3 src/quickbooks_sandbox.py` and review `output/quickbooks_payload_preview.json`.
3. Run `python3 -m unittest discover -s tests -v`; all tests must pass.
4. Confirm the seven account mappings in `config/quickbooks_accounts.csv`.

## Sandbox authorization

1. Sign in to the Intuit Developer dashboard.
2. Create or select an app with the QuickBooks Online Accounting scope.
3. Connect the app to a developer sandbox through Intuit's OAuth 2.0 Playground.
4. Obtain a short-lived access token and the sandbox company ID (`realmId`).
5. Store them only for the current local session as `QBO_ACCESS_TOKEN` and `QBO_REALM_ID`. Never paste them into repository files, screenshots, issues, or commits.

## Post and verify

Run `python3 src/quickbooks_sandbox.py --post`. The connector will:

1. Read the sandbox chart of accounts.
2. Create or reuse the seven AK Labs accounts.
3. Post 12 balanced journal entries from the eligible transaction set.
4. Retrieve each journal entry from QuickBooks.
5. Verify 24 lines, $6,854.06 in debits, $6,854.06 in credits, a $0.00 journal imbalance, and a $0.00 sandbox-to-source difference.

## Evidence and security

- `output/quickbooks_sandbox_reconciliation.csv` is the shareable control summary created only after a successful read-back.
- `output/quickbooks_sandbox_private.json` contains raw sandbox responses and is excluded from Git.
- Revoke or allow the short-lived access token to expire after testing.
- Do not describe the implementation as complete until the shareable reconciliation file exists and its values pass review.

## Troubleshooting

- `401` or `AuthenticationFailed`: refresh the OAuth access token.
- `403`: confirm the app has the QuickBooks Online Accounting scope and is connected to the selected sandbox.
- Account validation error: verify the configured account type is accepted by the sandbox company.
- Balance or source difference: stop; do not treat the run as successful until both differences are $0.00.
