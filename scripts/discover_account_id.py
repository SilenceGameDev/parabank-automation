from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from pages.transfer_funds_page import TransferFundsPage
from config import MY_TEST_USER
from logger import logger

def discover_known_account_id(driver) -> str:
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)

    accounts_page = AccountsOverviewPage(driver)
    accounts_page.load_transfer_funds_page()

    transfer = TransferFundsPage(driver)
    # assumes original account stays at index 0; new accounts append after it
    account_id = transfer.get_option_values(transfer.FROM_ACCOUNT)[0]
    logger.info(f"Discovered known account ID: {account_id}")
    return account_id