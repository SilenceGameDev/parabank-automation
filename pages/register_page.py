from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FIRST_NAME = (By.ID, "customer.firstName")
    LAST_NAME = (By.ID, "customer.lastName")
    ADDRESS = (By.ID, "customer.address.street")
    CITY = (By.ID, "customer.address.city")
    STATE = (By.ID, "customer.address.state")
    ZIP_CODE = (By.ID, "customer.address.zipCode")
    PHONE_NUMBER = (By.ID, "customer.phoneNumber")
    SSN = (By.ID, "customer.ssn")
    USERNAME = (By.ID, "customer.username")
    PASSWORD = (By.ID, "customer.password")
    CONFIRM_PASSWORD = (By.ID, "repeatedPassword")
    REGISTER_BUTTON = (By.XPATH, '//*[@id="customerForm"]/table/tbody/tr[13]/td[2]/input')
    WELCOME_TEXT = (By.XPATH, '//*[@id="rightPanel"]/h1')
    USER_EXISTS_ERROR = (By.ID, "customer.username.errors")

    def register_user(self,username, password):
        self.driver.get(self.URL)
        self.click(self.REGISTER_LINK)
        self.type(self.FIRST_NAME,"fname")
        self.type(self.LAST_NAME, "lname")
        self.type(self.ADDRESS, "address")
        self.type(self.CITY, "city")
        self.type(self.STATE, "state")
        self.type(self.ZIP_CODE, "123")
        self.type(self.PHONE_NUMBER, "456")
        self.type(self.SSN, "789")
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.type(self.CONFIRM_PASSWORD, password)
        self.click(self.REGISTER_BUTTON)

    def get_confirmation_text(self):
        return self.find(self.WELCOME_TEXT).text

    def get_error_text(self):
        return self.find(self.USER_EXISTS_ERROR).text