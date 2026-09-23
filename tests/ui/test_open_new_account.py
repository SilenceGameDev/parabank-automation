from pages.open_new_account_page import OpenNewAccountPage
import pytest
from pages.transfer_funds_page import TransferFundsPage


def test_open_new_checking_account(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_open_new_account_page()

    open_new_account_page = OpenNewAccountPage(driver)
    open_new_account_page.open_new_account(account_type_index=0)
    assert "Account Opened" in open_new_account_page.get_confirmation_text()

def test_open_new_savings_account(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_open_new_account_page()

    open_new_account_page = OpenNewAccountPage(driver)
    open_new_account_page.open_new_account(account_type_index=1)
    assert "Account Opened" in open_new_account_page.get_confirmation_text()

@pytest.mark.xfail(reason="ParaBank creates $100 from nothing when funding account can't cover it — see GitHub Issue #<6>")
def test_open_account_insufficient_funds_rejected(driver, logged_in_accounts_page, low_balance_account):
    logged_in_accounts_page.load_open_new_account_page()
    open_new_account_page = OpenNewAccountPage(driver)

    from_index = open_new_account_page.get_option_index_by_value(
        open_new_account_page.FROM_ACCOUNT, low_balance_account["account_id"]
    )
    open_new_account_page.open_new_account(account_type_index=0, from_index=from_index)
    assert "error" in open_new_account_page.get_confirmation_text().lower()