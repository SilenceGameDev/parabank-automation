from selenium.webdriver.common.by import By
from .base_page import BasePage

class AccountsOverviewPage(BasePage):
    TRANSFER_FUNDS_LINK_TEXT = (By.LINK_TEXT, "Transfer Funds")
    OPEN_ACCOUNT_LINK_TEXT = (By.LINK_TEXT, "Open New Account")
    BILL_PAY_LINK_TEXT = (By.LINK_TEXT, "Bill Pay")
    FIND_TRANSACTION_LINK_TEXT = (By.LINK_TEXT, "Find Transactions")

    def load_transfer_funds_page(self):
        self.click(self.TRANSFER_FUNDS_LINK_TEXT)

    def load_open_new_account_page(self):
        self.click(self.OPEN_ACCOUNT_LINK_TEXT)

    def load_bill_pay_page(self):
        self.click(self.BILL_PAY_LINK_TEXT)

    def load_find_transaction_page(self):
        self.click(self.FIND_TRANSACTION_LINK_TEXT)