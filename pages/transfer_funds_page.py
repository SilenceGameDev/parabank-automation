from selenium.webdriver.common.by import By
from .base_page import BasePage

class TransferFundsPage(BasePage):
    TRANSFER_COMPLETE = (By.CSS_SELECTOR, 'div#showResult h1.title')
    AMOUNT_INPUT_FIELD = (By.ID, "amount")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    TO_ACCOUNT = (By.ID, "toAccountId")
    TRANSFER_BUTTON = (By.CSS_SELECTOR, "input.button")

    def transfer_funds(self, amount_to_transfer:float, from_index:int=0, to_index:int=1):
        self.type(self.AMOUNT_INPUT_FIELD, str(amount_to_transfer))
        self.select_by_index(self.FROM_ACCOUNT, from_index)
        self.select_by_index(self.TO_ACCOUNT, to_index)
        self.click(self.TRANSFER_BUTTON)

    def get_confirmation_text(self):
        return self.find(self.TRANSFER_COMPLETE).text

