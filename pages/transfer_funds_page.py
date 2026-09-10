from selenium.webdriver.common.by import By
from .base_page import BasePage

class TransferFundsPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    TRANSFERFUNDS_BTN = (By.CSS_SELECTOR, "input.button")
    ERROR = (By.CSS_SELECTOR, ".error")

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

# login -- create login page class and login
# click transfer funds -- create accounts_overview page class and click transfer funds
# find amount text input field --
# input 7
# find From account dropdown and select 12345
# find To account dropdown and select 12456
# find Transfer button and click it