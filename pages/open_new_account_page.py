from selenium.webdriver.common.by import By
from .base_page import BasePage

class OpenNewAccountPage(BasePage):
    ACCOUNT_OPENED_TEXT = (By.XPATH, '//*[@id="openAccountResult"]/h1')
    ACCOUNT_TYPE = (By.ID, "type")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    OPEN_NEW_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "input.button")

    def open_new_account(self, account_type_index:int, from_index:int=0):
        self.select_by_index(self.ACCOUNT_TYPE, account_type_index)
        self.select_by_index(self.FROM_ACCOUNT, from_index)
        self.click(self.OPEN_NEW_ACCOUNT_BUTTON)

    def get_confirmation_text(self):
        return self.find(self.ACCOUNT_OPENED_TEXT).text
