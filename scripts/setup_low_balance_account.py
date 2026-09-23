from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.open_new_account_page import OpenNewAccountPage
from pages.transfer_funds_page import TransferFundsPage
from api.rest_client import ParaBankAPI
from config import MY_TEST_USER
from logger import logger

api = ParaBankAPI()
DRAIN_TARGET = 1.00  # leave $1 — enough to exist, not enough to fund a $100 open-account debit


def get_account_balance(account_id: str) -> float:
    resp = api.get_account(account_id)
    resp.raise_for_status()
    return float(resp.json()["balance"])


def create_low_balance_account(driver) -> str:
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)

    accounts_page = AccountsOverviewPage(driver)

    # Step 1: open a fresh account — starts at a known $100
    accounts_page.load_open_new_account_page()
    open_account = OpenNewAccountPage(driver)
    open_account.open_new_account(account_type_index=0, from_index=0)
    if "Account Opened" not in open_account.get_confirmation_text():
        raise RuntimeError("Failed to create low-balance account — setup cannot continue")

    # Step 2: confirm it actually exists via the API — real existence check,
    # not just trusting the UI's success message
    accounts_page.load_transfer_funds_page()
    transfer = TransferFundsPage(driver)
    new_account_id = transfer.get_last_account_option_value(transfer.FROM_ACCOUNT)
    starting_balance = get_account_balance(new_account_id)
    logger.info(f"Created account {new_account_id}, starting balance ${starting_balance:.2f}")

    # Step 3: drain it — exactly once, since this function only runs once
    # per session (see the session-scoped fixture in conftest.py)
    amount_to_drain = starting_balance - DRAIN_TARGET
    if amount_to_drain > 0:
        from_index = transfer.get_option_index_by_value(transfer.FROM_ACCOUNT, new_account_id)
        transfer.transfer_funds(amount_to_transfer=amount_to_drain, from_index=from_index, to_index=0)

    # Step 4: confirm the drain actually worked — second API check, not assumed
    ending_balance = get_account_balance(new_account_id)
    if ending_balance > DRAIN_TARGET + 0.01:
        raise RuntimeError(
            f"Drain failed — expected balance <= ${DRAIN_TARGET:.2f}, got ${ending_balance:.2f}"
        )
    logger.info(f"Confirmed: account {new_account_id} now at ${ending_balance:.2f}")

    return new_account_id