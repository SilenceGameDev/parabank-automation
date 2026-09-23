from pages.find_transactions_page import FindTransactionsPage
import pytest

def test_find_by_transaction_id(driver, logged_in_accounts_page, known_transaction):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_transaction_id(transaction_id=known_transaction["id"])
    assert "Transaction Results" in find_transactions_page.get_confirmation_text()

def test_find_by_date_range(driver, logged_in_accounts_page, known_transaction):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_date_range(from_date=known_transaction["date"], to_date=known_transaction["date"])
    assert "Transaction Results" in find_transactions_page.get_confirmation_text()

def test_find_by_amount(driver, logged_in_accounts_page, known_transaction):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_amount(amount=known_transaction["amount"])
    assert "Transaction Results" in find_transactions_page.get_confirmation_text()

def test_find_by_transaction_id_invalid_id(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_transaction_id(transaction_id="abc")
    assert "Invalid transaction ID" in find_transactions_page.get_specific_error_text("id")

def test_find_by_transaction_date_range_invalid_dates(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_date_range(from_date="abc", to_date="123")
    assert "Invalid date format" in find_transactions_page.get_specific_error_text("date_range")

def test_find_by_transaction_amount_invalid_amount(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_amount(amount="abc")
    assert "Invalid amount" in find_transactions_page.get_specific_error_text("amount")

@pytest.mark.xfail(reason="ParaBank shows 'NaN' instead of a proper no-results message — see GitHub Issue #7")
def test_find_by_transaction_date_range_non_existent(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_date_range(from_date="01-01-1999", to_date="01-01-2000")
    assert "No transactions found" in find_transactions_page.get_confirmation_text()  # what *should* happen

@pytest.mark.xfail(reason="ParaBank shows 'NaN' instead of a proper no-results message — see GitHub Issue #7")
def test_find_by_transaction_amount_non_existent(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_find_transaction_page()
    find_transactions_page = FindTransactionsPage(driver)
    find_transactions_page.find_by_amount(amount="2")
    assert "NaN" in find_transactions_page.get_specific_error_text("nan")