from selenium.webdriver.common.by import By
from .base_page import BasePage

class AccountsOverviewPage(BasePage):
    TRANSFER_FUNDS_LINK_TEXT = (By.LINK_TEXT, "transfer.htm")
    OPEN_ACCOUNT_LINK_TEXT = (By.LINK_TEXT, "openaccount.htm")
    BILL_PAY_LINK_TEXT = (By.LINK_TEXT, "billpay.htm")
    FIND_TRANSACTION_LINK_TEXT = (By.LINK_TEXT, "findtrans.htm")

    def transfer_funds(self):
        self.click(self.TRANSFER_FUNDS_LINK_TEXT)

    def open_new_account(self):
        self.click(self.OPEN_ACCOUNT_LINK_TEXT)

    def bill_pay(self):
        self.click(self.BILL_PAY_LINK_TEXT)

    def find_transaction(self):
        self.click(self.FIND_TRANSACTION_LINK_TEXT)