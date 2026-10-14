# Test Plan — ParaBank QA Automation Framework

---

## 1. Document Info

| Field | Value                            |
|---|----------------------------------|
| Project name | ParaBank QA Automation Framework |
| Author | Trevaughn Primus                 |
| Date | 9/5/2026                         |
| Version | v1.0                             |
| Target role this supports | QA Automation Engineer           |

## 2. Objective

Demonstrate Selenium-based UI automation, REST and SOAP API testing, negative/boundary test design, and CI integration against a banking-style application, to close the automation-tool and finance-domain gaps identified against the OneStream Software QA Engineer II posting.

## 3. Scope

**In scope:**
- Login / authentication
- Account overview
- Fund transfers between accounts
- Opening a new account
- Bill pay
- Finding/searching transactions
- REST API endpoints for accounts and transactions
- SOAP API endpoints (parity check against REST where applicable)

**Out of scope:**
- Performance/load testing — Basic usability is the focus of this small project.
- JMS messaging features — Not enough time to properly test async features
- Mobile browser testing — This would include a wide variety of phones, not suitable for a portfolio project like this


## 4. Test Approach

| Test type | Included? | Notes                                 |
|---|-----------|---------------------------------------|
| Functional (UI) | Y         | Selenium + pytest, Page Object Model  |
| API (REST) | Y         | `requests` library                    |
| API (SOAP) | Y         | `zeep` library                        |
| Negative / boundary | Y         | See flagged rows in Section 6         |
| Regression | Y         | Re-run full suite on each change      |
| Data-driven / parametrized | Y         | Transfer amount boundaries at minimum |
| Performance | N         | Out of scope for this project         |
| Security | Y         | SQL-injection checks                  |

## 5. Environment & Tools

| Category | Tool/Detail                                                                                     |
|---|-------------------------------------------------------------------------------------------------|
| Application under test | ParaBank — https://parabank.parasoft.com/parabank/index.htm                                     |
| Test login | Dedicated test account registered specifically for this project, using fake/placeholder profile data. Credentials stored in .env (not committed — see README setup instructions). Shared demo login (john/demo) retained in test_data/users.json for scenarios where account-specific state doesn't matter. |
| Language | Python 3.14                                                                                     |
| Test framework | pytest                                                                                          |
| UI automation | Selenium WebDriver                                                                              |
| API tooling | `requests` (REST), `zeep` (SOAP)                                                                |
| CI/CD | GitHub Actions [add Azure Pipelines if doing the stretch goal]                                  |
| Reporting | pytest-html [or Allure, if going further]                                                       |
| IDE | PyCharm                                                                                         |
| Browser(s) | Chrome, headless in CI                                                                          |

## 6. Features / Items to Be Tested

*Priority and Expected Result columns are left for you to fill in. Add rows for anything specific to your build.*

### Login / Authentication

| ID     | Test case                                                                     | Priority | Expected Result                                           |
|--------|-------------------------------------------------------------------------------|----------|-----------------------------------------------------------|
| TC-001 | Login with valid username/password                                            | High     | Successful Login                                          |
| TC-002 | Login with valid username, incorrect password                                 | High     | Reject Login and display related help message             |
| TC-003 | Login with empty username and/or password fields                              | High     | Reject login and display related help message             |
| TC-004 | Login with username containing special characters / SQL-injection-style input | High     | Reject login and display related help message             |
| TC-005 | Session behavior after login (redirect to account overview)                   | Medium   | User is redirected to the appropriate page                |
| TC-006 | Logout/session-expiry                                                         | High     | **Not automated.** No logout or session-expiry test currently exists in `test_login.py`. |

### Account Overview

| ID | Test case | Priority | Expected Result                                                                   |
|---|---|----------|-----------------------------------------------------------------------------------|
| TC-007 | Verify all accounts for logged-in user are listed with correct balances | High     | All accounts are visible and display the correct balance                          |
| TC-008 | Click into an individual account and verify details load correctly | High     | All account details are correct. Showing account number, balance and transactions |

### Fund Transfers

| ID | Test case | Priority | Expected Result                                                           |
|---|---|----------|---------------------------------------------------------------------------|
| TC-009 | Transfer a valid amount between two owned accounts | High     | The valid amount is transfered and both accounts update correctly         |
| TC-010 | Transfer amount of $0 | Medium   | **Confirmed wrong:** ParaBank completes the transfer with no validation error instead of rejecting it. See Issue #2. Automated as `xfail` (`test_zero_amount_transfer_rejected`). |
| TC-011 | Transfer a negative amount | High     | Manually confirmed to exhibit the same missing-validation behavior as TC-010 (Issue #2). No dedicated automated test — zero-amount is treated as the representative case for this defect. |
| TC-012 | Transfer amount exceeding account balance | High     | Manually confirmed to exhibit the same missing-validation behavior as TC-010 (Issue #2). No dedicated automated test. |
| TC-013 | Transfer amount with non-numeric input | High     | Not manually verified against this specific defect; expected to be rejected by client-side/type validation before reaching the same code path as TC-010–012. Not automated. |
| TC-014 | Verify balances update correctly on both accounts after a valid transfer | High     | Both accounts update correctly                                            |
| TC-015 | Transfer to/from the same account | Medium   | Message appears telling the user to select a valid account to transfer to |

### Open New Account

| ID | Test case | Priority | Expected Result                                                                      |
|---|---|----------|--------------------------------------------------------------------------------------|
| TC-016 | Open new Checking account funded from an existing account | High     | New checking account appears                                                         |
| TC-017 | Open new Savings account funded from an existing account | High     | New Savings account appears                                                          |
| TC-018 | Attempt to open account with insufficient funding account balance | High     | **Confirmed wrong, most severe finding in the project:** account creation *does* complete, the funding account goes negative, and the new account still receives the full $100, an accounting-integrity failure, not just a missing validation message. See Issue #6. Automated as `xfail` (`test_open_account_insufficient_funds_rejected`), using a dedicated drained-balance account. |
| TC-019 | Verify new account appears in Account Overview immediately after creation | High     | New account appears in Account Overview                                              |

### Bill Pay

| ID | Test case | Priority | Expected Result                                                             |
|---|---|----------|-----------------------------------------------------------------------------|
| TC-020 | Submit bill payment with all required fields valid | High     | Message appears confirming successful payment                               |
| TC-021 | Submit bill payment with missing required field(s) | High     | Message appears tell the user there is missing information                  |
| TC-022 | Submit bill payment with invalid data format (e.g. letters in zip/phone) | High     | Message appears telling the user to enter valid data                        |
| TC-023 | Submit bill payment amount exceeding account balance | High     | **Confirmed wrong:** ParaBank completes the payment with no validation error. See Issue #5 (same pattern as Transfer Funds, Issue #2). Automated as `xfail` (`test_zero_amount_bill_pay_rejected`) — zero-amount is the representative case tested; exceeding-balance specifically was manually confirmed but not separately automated. |

### Find Transactions

| ID | Test case | Priority | Expected Result                                                 |
|---|---|---|-----------------------------------------------------------------|
| TC-024 | Search transactions by date range |Medium | Transactions are sorted by date                                 |
| TC-025 | Search transactions by amount |Medium | Transactions are sorted by amount                               |
| TC-026 | Search transactions by transaction ID |Medium | Transactions are sorted by transaction ID                       |
| TC-027 | Search with no matching results |Medium | Message appears telling user no transactions match their search |

### REST API

| ID | Test case | Priority | Expected Result                                                                                                                   |
|---|---|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| TC-028 | GET account details by valid account ID — verify 200 and response schema | High     | Valid response code is returned along with account details                                                                        |
| TC-029 | GET account details by invalid/nonexistent account ID | High     | **Updated from original assumption:** no application-level "message," this is a REST API. Confirmed actual behavior: `400` for a valid-format-but-nonexistent numeric ID (e.g. `999999999`, `-1`), `404` for a non-numeric ID (e.g. `abc`). See Issue #1. Automated via a parametrized test covering all three cases. |
| TC-030 | GET transactions for a valid account ID | High     | Confirmed: 200 with transaction data. Same 400/404 invalid-ID split as TC-029 confirmed here too (Issue #1). |
| TC-031 | GET request with missing/invalid auth (if applicable) | Medium   | **Not automated.** ParaBank's REST endpoints don't appear to require an auth header at all based on testing so far; left here as an open question rather than removed. |
| TC-032 | Verify response times are within acceptable range | High     | Response times are 5 seconds or less. Generous threshold given shared public demo instance, not representative of a production SLA |

### SOAP API

| ID | Test case | Priority | Expected Result                                        |
|---|---|----------|--------------------------------------------------------|
| TC-033 | getAccount via SOAP — verify response matches REST equivalent | High     | SOAP response matches REST equivalent                  |
| TC-034 | SOAP request with invalid account ID | High     | **Not automated.** Only the happy-path SOAP call and the REST/SOAP parity check (TC-035) are currently implemented. |
| TC-035 | Compare REST vs. SOAP response for same data — document any discrepancies | Medium   | Responses between the two are the same or very similar |

### Cross-Cutting

| ID     | Test case | Priority | Expected Result                             |
|--------|---|----------|---------------------------------------------|
| TC-036 | Full regression suite runs green in CI on a clean checkout | High     | No new issues encountered                   |
| TC-037 | Perform a transfer via the UI                                                           | High     | **Not automated.** Discussed as a valuable cross-layer end-to-end test (proves UI actions are reflected correctly at the API level) but not yet built. |

## 7. Entry / Exit Criteria

**Entry criteria:**
- ParaBank public instance is reachable and login works
- Local framework environment (PyCharm, venv, dependencies) is set up and a smoke test passes

**Exit criteria:**
- All Priority: High test cases automated and passing, or logged as known issues
- CI pipeline runs green on main branch
- At least 5 defects/observations documented

## 8. Defect Management

- Tool: GitHub Issues
- Format: Title / Steps to reproduce / Expected vs. actual / Severity / Evidence
- Target: Document at least 3-5 real findings

## 9. Risks & Assumptions

| Risk/Assumption                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Impact   | Mitigation                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Registered account may still be affected by ParaBank-side resets/maintenance, but is no longer shared with concurrent tutorial users                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Low      | Using a dedicated registered account instead of the shared john/demo login eliminates interference from other users' simultaneous test activity. Note in README if ParaBank performs a full data reset.                                                                                                                                                                                                                                                       |
| Limited control over backend state/data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Low      | Dedicated account means data only changes as a result of this test suite's own actions — still verify current state via API before balance-dependent assertions rather than hardcoding expected values, since test run order can still affect state across runs                                                                                                                                                                                               |
| The public ParaBank instance is periodically reset by Parasoft, which can wipe registered accounts entirely (confirmed via Parasoft's own forums, and observed directly during this project when a registered account disappeared after ~1 day).<br/>Observed escalation: on 9/14/2026, the instance didn't just reset account data, it returned a generic "An internal error has occurred" on login and on every subsequent link, for all accounts (old and newly-created), for approximately 24 hours. This confirms the shared instance can experience full outages, not just data resets, with no visible status page or ETA.  | Medium   | Document account re-registration as a known setup step in the README; avoid hardcoding a specific account's data as a long-term fixture — treat account creation as something the test suite (or a setup script) may need to redo periodically. <br/>Treat "ParaBank is down" as a real possibility during any test run, not just "my account needs re-registering". A full CI run could fail entirely on a day like this, through no fault of the test code. |
|   Authentication may silently fail to validate credentials, granting access to an unintended account regardless of input (observed [date], see Issue #__)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Critical |    Before trusting any test result during a session, verify the logged-in account's identity (account owner, account IDs) matches the expected user, rather than relying solely on a successful redirect to confirm correct authentication                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

## 10. Deliverables

- Test plan (this document)
- Automated test suite (GitHub repo link)
- CI pipeline configuration
- Test report
- Documented defects (3-5 minimum)
- README
- Resume/cover letter line referencing this project

## 11. Schedule

| Milestone | Target date |
|---|-------------|
| Test plan finalized | 9/5/2026    |
| Framework scaffolded (PyCharm, POM structure) | 9/12/2026   |
| UI test cases automated | 9/12/2026   |
| API test cases automated (REST + SOAP) | 9/19/2026   |
| CI pipeline live | 9/19/2026   |
| Defects documented | 9/19/2026   |
| README/portfolio polish complete | 9/19/2026   |