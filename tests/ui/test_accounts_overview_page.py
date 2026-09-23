from pages.accounts_overview_page import AccountsOverviewPage

def test_load_transfer_funds_page(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_transfer_funds_page()
    assert "transfer.htm" in driver.current_url

def test_load_open_new_account_page(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_open_new_account_page()

    assert "openaccount.htm" in driver.current_url

def test_load_bill_pay_page(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()
    assert "billpay.htm" in driver.current_url

def test_load_find_transaction_page(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    assert "findtrans.htm" in driver.current_url