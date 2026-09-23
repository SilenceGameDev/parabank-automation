from datetime import date
from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.transfer_funds_page import TransferFundsPage
from api.rest_client import ParaBankAPI
from config import MY_TEST_USER
from logger import logger

api = ParaBankAPI()
TRANSFER_AMOUNT = 5.00  # arbitrary, small, safe — used purely to generate a known transaction


def generate_known_transaction(driver, account_id: str) -> dict:
    """Performs a small transfer to guarantee a fresh, real transaction exists,
    then confirms its actual ID via the REST API. Date and amount are known
    up front since we control them; only the ID is server-generated."""
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)

    accounts_page = AccountsOverviewPage(driver)
    accounts_page.load_transfer_funds_page()

    transfer = TransferFundsPage(driver)
    from_index = transfer.get_option_index_by_value(transfer.FROM_ACCOUNT, account_id)
    transfer.transfer_funds(amount_to_transfer=TRANSFER_AMOUNT, from_index=from_index, to_index=0)

    if "Transfer Complete" not in transfer.get_confirmation_text():
        raise RuntimeError("Failed to generate known transaction — transfer did not complete")

    # Confirm via API rather than scraping the UI for the ID
    resp = api.get_transactions(account_id)
    resp.raise_for_status()
    transactions = resp.json()
    logger.info(f"Transactions for account {account_id}: {transactions}")

    latest = transactions[-1]

    return {
        "id": str(latest["id"]),
        "date": date.today().strftime("%m-%d-%Y"),
        "amount": str(TRANSFER_AMOUNT),
    }