from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input.button")
    ERROR = (By.CSS_SELECTOR, ".error")

    def load(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        # wait for the redirect to actually happen before returning
        self.wait.until(EC.url_contains("overview.htm"))

    def login_expecting_error(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        self.wait.until(EC.visibility_of_element_located(self.ERROR))