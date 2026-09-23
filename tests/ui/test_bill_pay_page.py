from pages.bill_pay_page import BillPayPage, PayeeInformation
import pytest

def test_enter_required_information(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation()
    bill_pay_page.enter_required_information(amount_to_pay="7",payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Bill Payment Complete" in bill_pay_page.get_confirmation_text()

@pytest.mark.xfail(reason="ParaBank accepts invalid bill payment amounts — see GitHub Issue #5")
def test_zero_amount_bill_pay_rejected(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation()
    bill_pay_page.enter_required_information(amount_to_pay="0",payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "error" in bill_pay_page.get_confirmation_text().lower()  # what *should* happen

def test_missing_payee_name(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_name="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Payee name is required" in bill_pay_page.get_specific_error_text("name")

def test_missing_address(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_address_street="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Address is required" in bill_pay_page.get_specific_error_text("address")

def test_missing_city(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_address_city="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "City is required" in bill_pay_page.get_specific_error_text("city")

def test_missing_state(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_address_state="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "State is required" in bill_pay_page.get_specific_error_text("state")

def test_missing_zip_code(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_address_zip_code="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Zip Code is required" in bill_pay_page.get_specific_error_text("zipcode")

def test_missing_phone(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_phone_number="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Phone number is required" in bill_pay_page.get_specific_error_text("phone")

def test_missing_account_number(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(payee_account_number="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Account number is required" in bill_pay_page.get_specific_error_text("account")

def test_missing_verify_account_number(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation(verify_account_number="")
    bill_pay_page.enter_required_information(amount_to_pay="7", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "Account number is required" in bill_pay_page.get_specific_error_text("verify")

def test_missing_amount(driver, logged_in_accounts_page):
    logged_in_accounts_page.load_bill_pay_page()

    bill_pay_page = BillPayPage(driver)
    payee_information = PayeeInformation()
    bill_pay_page.enter_required_information(amount_to_pay="", payee_information=payee_information)
    bill_pay_page.pay_bill()
    assert "The amount cannot be empty" in bill_pay_page.get_specific_error_text("amount")