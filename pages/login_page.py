from selenium.webdriver.common.by import By
from .base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "input.button")
    ERROR = (By.CSS_SELECTOR, ".title")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    WELCOME_TEXT = (By.CSS_SELECTOR, 'div#leftPanel p.smallText')

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

    def register(self, username, password):
        self.click(self.REGISTER_LINK)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)

    def get_error_text(self):
        return self.find(self.ERROR).text.lower()

    def get_welcome_text(self):
        return self.find(self.WELCOME_TEXT).text.lower()
