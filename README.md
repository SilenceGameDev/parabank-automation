# ParaBank QA Automation Framework

## Status - Complete
All planned test cases (or their documented gaps) reflect actual, verified ParaBank behavior as of 09/22/2026.

## Setup

1. Create your own `.env` file at the project root with your ParaBank credentials:

   ```
   PARABANK_TEST_USERNAME="your_username"
   PARABANK_TEST_PASSWORD="your_password"
   ```

2. That's it. You do **not** need to manually register an account first, on
   first run, the test suite automatically checks whether your account
   exists and registers it fresh if it doesn't (see `ensure_test_account.py`).

3. If you want to explore ParaBank manually outside the automated suite, you
   can register your own account directly at
   [parabank.parasoft.com/parabank/register.htm](https://parabank.parasoft.com/parabank/register.htm)
   using fake details, just note the username/password you choose. The
   shared public instance resets approximately once a day, so manual
   registrations will need to be redone periodically. This limitation
   doesn't affect automated runs, since the `.env`-based setup re-registers
   automatically every session if needed.

## Design Notes

- **Uses a dedicated test account** rather than the shared public demo
  login, to keep test data consistent and isolated across runs.
- **Account IDs, transaction IDs, and other test data are discovered live
  each session** via the UI and API rather than hardcoded, since the shared
  ParaBank instance resets unpredictably (see Risk in test plan Section 9).
  Hardcoded values were tried early in the project and broke every time the
  instance reset; this was the fix.

## Known Issues (ParaBank platform)

- **#1** — `GET /accounts/{id}` and `GET /accounts/{id}/transactions` both
  return `400` for a valid-format-but-nonexistent numeric ID, but `404` for
  a non-numeric ID, an inconsistent status code convention shared across
  both endpoints.
- **#2, #5, #6** — Transfer Funds, Bill Pay, and Open New Account all accept
  invalid amounts (zero, negative, exceeding balance) without a validation
  error, while field-presence validation (empty required fields) works
  correctly across the same forms.
- **#3** — Accounts Overview balance doesn't reflect a transfer until the
  individual account's activity is viewed directly. *(Documented but not
  covered by an automated test, a deliberate scope decision given the
  project's size.)*
- **#4** — Registration and login returned a generic "An internal error has
  occurred" for approximately 24 hours, affecting all accounts including
  newly-created ones. A full platform outage, not an account-specific issue.
- **#6** — The most severe finding: Open New Account creates 100 dollars of new
  value with no corresponding valid debit. The funding account goes
  negative while the new account still receives the full 100 dollars, an actual
  accounting-integrity failure, not just a missing validation message.
  (Related to #2, #3, #5.)
- **#7** — Find Transactions displays the literal text "NaN" instead of a
  proper "no results" message when a date-range or amount search matches
  nothing.

## Scope Notes

- **Registration** is exercised indirectly through automated test account
  setup (`ensure_test_account.py`) but has no dedicated test of its own,
  since testing registration directly would require a disposable account
  that doesn't collide with the persistent dedicated account every other
  test depends on.
- **Issue #3** (delayed balance display) is documented above but
  intentionally has no automated test, given the project's deliberately
  small scope.