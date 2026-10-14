from selenium.webdriver.common.by import By
from .base_page import BasePage

class FindTransactionsPage(BasePage):
    TRANSACTION_RESULTS_TEXT = (By.CSS_SELECTOR, 'div#resultContainer > h1.title')
    ACCOUNT_ID_DROPDOWN = (By.ID, "accountId")

    TRANSACTION_ID_FIELD = (By.ID, "transactionId")
    FIND_TRANSACTIONS_ID_BUTTON = (By.ID, "findById")

    FROM_DATE_FIELD = (By.ID,"fromDate")
    TO_DATE_FIELD = (By.ID,"toDate")
    FIND_BY_DATE_RANGE_BUTTON = (By.ID, "findByDateRange")

    AMOUNT_FIELD = (By.ID, "amount")
    FIND_BY_AMOUNT_BUTTON = (By.ID, "findByAmount")

    transaction_error_texts = {
        "id":(By.ID, "transactionIdError"),
        "date_range": (By.ID, "dateRangeError"),
        "amount": (By.ID, "amountError"),
        "nan": (By.CSS_SELECTOR, '#transactionTable tbody tr td')
    }

    def find_by_transaction_id(self, transaction_id:str, account_id_index:int=0):
        self.select_by_index(self.ACCOUNT_ID_DROPDOWN, account_id_index)
        self.type(self.TRANSACTION_ID_FIELD, transaction_id)
        self.click(self.FIND_TRANSACTIONS_ID_BUTTON)

    def find_by_date_range(self, from_date:str, to_date:str, account_id_index:int=0):
        self.select_by_index(self.ACCOUNT_ID_DROPDOWN, account_id_index)
        self.type(self.FROM_DATE_FIELD, from_date)
        self.type(self.TO_DATE_FIELD, to_date)
        self.click(self.FIND_BY_DATE_RANGE_BUTTON)

    def find_by_amount(self, amount:"str", account_id_index:int=0):
        self.select_by_index(self.ACCOUNT_ID_DROPDOWN, account_id_index)
        self.type(self.AMOUNT_FIELD, amount)
        self.click(self.FIND_BY_AMOUNT_BUTTON)

    def get_confirmation_text(self):
        return self.find(self.TRANSACTION_RESULTS_TEXT).text

    def get_specific_error_text(self, error_text:str):
        return self.find(self.transaction_error_texts[error_text]).text
