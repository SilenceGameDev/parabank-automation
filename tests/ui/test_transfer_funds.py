from pages.transfer_funds_page import TransferFundsPage
import pytest

def test_valid_transfer(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_transfer_funds_page()

    transfer = TransferFundsPage(driver)
    transfer.transfer_funds(amount_to_transfer=7)
    assert "Transfer Complete" in transfer.get_confirmation_text()

@pytest.mark.xfail(reason="ParaBank accepts invalid transfer amounts — see GitHub Issue #2")
def test_zero_amount_transfer_rejected(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_transfer_funds_page()

    transfer = TransferFundsPage(driver)
    transfer.transfer_funds(amount_to_transfer=0)
    assert "error" in transfer.get_confirmation_text().lower()  # what *should* happen
