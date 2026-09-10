# Test Plan — ParaBank QA Automation Framework

---

## 1. Document Info

| Field | Value |
|---|---|
| Project name | ParaBank QA Automation Framework |
| Author | [Your Name] |
| Date | [Date] |
| Version | v1.0 |
| Target role this supports | Software QA Engineer II — OneStream Software |

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
-  Performance/load testing — Basic usability is the focus of this small project.
-  JMS messaging features — Not enough time to properly test async features
-  Mobile browser testing — This would include a wide variety of phones, not suitable for a portfolio project like this


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
| TC-006 | Logout/session-expiry                                                         | High     | User logout or session expires correctly log the user out |

### Account Overview

| ID | Test case | Priority | Expected Result                                                                   |
|---|---|----------|-----------------------------------------------------------------------------------|
| TC-007 | Verify all accounts for logged-in user are listed with correct balances | High     | All accounts are visible and display the correct balance                          |
| TC-008 | Click into an individual account and verify details load correctly | High     | All account details are correct. Showing account number, balance and transactions |

### Fund Transfers

| ID | Test case | Priority | Expected Result                                                           |
|---|---|----------|---------------------------------------------------------------------------|
| TC-009 | Transfer a valid amount between two owned accounts | High     | The valid amount is transfered and both accounts update correctly         |
| TC-010 | Transfer amount of $0 | Medium   | Message appears telling the user to enter a valid dollar amount           |
| TC-011 | Transfer a negative amount | High     | Message appears telling the user to enter a valid dollar amount           |
| TC-012 | Transfer amount exceeding account balance | High     | Message appears telling the user to enter a valid dollar amount           |
| TC-013 | Transfer amount with non-numeric input | High     | Message appears telling the user to enter a valid dollar amount           |
| TC-014 | Verify balances update correctly on both accounts after a valid transfer | High     | Both accounts update correctly                                            |
| TC-015 | Transfer to/from the same account | Medium   | Message appears telling the user to select a valid account to transfer to |

### Open New Account

| ID | Test case | Priority | Expected Result                                                                      |
|---|---|----------|--------------------------------------------------------------------------------------|
| TC-016 | Open new Checking account funded from an existing account | High     | New checking account appears                                                         |
| TC-017 | Open new Savings account funded from an existing account | High     | New Savings account appears                                                          |
| TC-018 | Attempt to open account with insufficient funding account balance | High     | Creation does not complete. Message appears telling user about insufficient funding |
| TC-019 | Verify new account appears in Account Overview immediately after creation | High     | New account appears in Account Overview                                              |

### Bill Pay

| ID | Test case | Priority | Expected Result                                                             |
|---|---|----------|-----------------------------------------------------------------------------|
| TC-020 | Submit bill payment with all required fields valid | High     | Message appears confirming successful payment                               |
| TC-021 | Submit bill payment with missing required field(s) | High     | Message appears tell the user there is missing information                  |
| TC-022 | Submit bill payment with invalid data format (e.g. letters in zip/phone) | High     | Message appears telling the user to enter valid data                        |
| TC-023 | Submit bill payment amount exceeding account balance | High     | Message appears telling the user why they are unable to complete the action |

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
| TC-029 | GET account details by invalid/nonexistent account ID | High     | ID not found message appears                                                                                                      |
| TC-030 | GET transactions for a valid account ID | High     | Transactions appear                                                                                                                |
| TC-031 | GET request with missing/invalid auth (if applicable) | Medium   | Message appears telling user to enter valid authentication                                                                        |
| TC-032 | Verify response times are within acceptable range | High     | Response times are 5 seconds or less. Generous threshold given shared public demo instance, not representative of a production SLA |

### SOAP API

| ID | Test case | Priority | Expected Result                                        |
|---|---|----------|--------------------------------------------------------|
| TC-033 | getAccount via SOAP — verify response matches REST equivalent | High     | SOAP response matches REST equivalent                  |
| TC-034 | SOAP request with invalid account ID | High     | Message appears telling user invalid account ID        |
| TC-035 | Compare REST vs. SOAP response for same data — document any discrepancies | Medium   | Responses between the two are the same or very similar |

### Cross-Cutting

| ID     | Test case | Priority | Expected Result                             |
|--------|---|----------|---------------------------------------------|
| TC-036 | Full regression suite runs green in CI on a clean checkout | High     | No new issues encountered                   |
| TC-037 | Perform a transfer via the UI                                                           | High     | Verify the updated balance via the REST API |

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

| Risk/Assumption | Impact | Mitigation                                                                                                 |
|---|--------|------------------------------------------------------------------------------------------------------------|
| Registered account may still be affected by ParaBank-side resets/maintenance, but is no longer shared with concurrent tutorial users | Low    | Using a dedicated registered account instead of the shared john/demo login eliminates interference from other users' simultaneous test activity. Note in README if ParaBank performs a full data reset.                     |
| Limited control over backend state/data | Low    | Dedicated account means data only changes as a result of this test suite's own actions — still verify current state via API before balance-dependent assertions rather than hardcoding expected values, since test run order can still affect state across runs |
|  The public ParaBank instance is periodically reset by Parasoft, which can wipe registered accounts entirely (confirmed via Parasoft's own forums, and observed directly during this project when a registered account disappeared after ~1 day)                                       | Medium | Document account re-registration as a known setup step in the README; avoid hardcoding a specific account's data as a long-term fixture — treat account creation as something the test suite (or a setup script) may need to redo periodically                                                                                                                                                                                                                                                                |

## 10. Deliverables

-  Test plan (this document)
-  Automated test suite (GitHub repo link)
-  CI pipeline configuration
-  Test report
-  Documented defects (3-5 minimum)
-  README
-  Resume/cover letter line referencing this project

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
