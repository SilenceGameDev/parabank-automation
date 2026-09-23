from selenium.webdriver.common.by import By
from .base_page import BasePage
from dataclasses import dataclass

# Used to quickly populate PayeeInformation
@dataclass
class PayeeInformation:
    payee_name: str = "name"
    payee_address_street: str = "street"
    payee_address_city: str = "city"
    payee_address_state: str = "state"
    payee_address_zip_code: str = "77777"
    payee_phone_number: str = "12345"
    payee_account_number: str = "6789"
    verify_account_number: str = "6789"

class BillPayPage(BasePage):
    BILL_PAYMENT_COMPLETE = (By.XPATH, '//*[@id="billpayResult"]/h1')
    PAYEE_NAME = (By.NAME, "payee.name")
    PAYEE_ADDRESS_STREET = (By.NAME, "payee.address.street")
    PAYEE_ADDRESS_CITY = (By.NAME, "payee.address.city")
    PAYEE_ADDRESS_STATE = (By.NAME, "payee.address.state")
    PAYEE_ADDRESS_ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PAYEE_PHONE_NUMBER = (By.NAME, "payee.phoneNumber")
    PAYEE_ACCOUNT_NUMBER = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT_NUMBER = (By.NAME, "verifyAccount")
    AMOUNT_TO_PAY = (By.NAME, "amount")
    FROM_ACCOUNT = (By.NAME, "fromAccountId")
    SEND_PAYMENT_BUTTON = (By.CSS_SELECTOR, "input.button")

    PAYEE_NAME_ERROR = (By.ID, "validationModel-name")
    ADDRESS_STREET_ERROR = (By.ID, "validationModel-address")
    CITY_ERROR = (By.ID, "validationModel-city")
    STATE_ERROR = (By.ID, "validationModel-state")
    ZIP_CODE_ERROR = (By.ID, "validationModel-zipCode")
    PHONE_NUMBER_ERROR = (By.ID, "validationModel-phoneNumber")
    ACCOUNT_NUMBER_ERROR = (By.ID, "validationModel-account-empty")
    VERIFY_ACCOUNT_NUMBER_ERROR = (By.ID, "validationModel-verifyAccount-empty")
    AMOUNT_TO_PAY_ERROR = (By.ID, "validationModel-amount-empty")

    error_text_dict = {
        "name": PAYEE_NAME_ERROR, "address": ADDRESS_STREET_ERROR, "city": CITY_ERROR, "state": STATE_ERROR,
        "zipcode": ZIP_CODE_ERROR, "phone": PHONE_NUMBER_ERROR, "account": ACCOUNT_NUMBER_ERROR,
        "verify": VERIFY_ACCOUNT_NUMBER_ERROR, "amount": AMOUNT_TO_PAY_ERROR,
                       }

    def enter_required_information(self, amount_to_pay:str, payee_information:PayeeInformation,from_index:int=0):
        self.type(self.PAYEE_NAME, payee_information.payee_name)
        self.type(self.PAYEE_ADDRESS_STREET, payee_information.payee_address_street)
        self.type(self.PAYEE_ADDRESS_CITY, payee_information.payee_address_city)
        self.type(self.PAYEE_ADDRESS_STATE, payee_information.payee_address_state)
        self.type(self.PAYEE_ADDRESS_ZIP_CODE, payee_information.payee_address_zip_code)
        self.type(self.PAYEE_PHONE_NUMBER, payee_information.payee_phone_number)
        self.type(self.PAYEE_ACCOUNT_NUMBER, payee_information.payee_account_number)
        self.type(self.VERIFY_ACCOUNT_NUMBER, payee_information.verify_account_number)
        self.type(self.AMOUNT_TO_PAY,amount_to_pay)
        self.select_by_index(self.FROM_ACCOUNT, from_index)

    def pay_bill(self):
        self.click(self.SEND_PAYMENT_BUTTON)

    def get_confirmation_text(self):
        return self.find(self.BILL_PAYMENT_COMPLETE).text

    def get_specific_error_text(self, error_text_key:str):
        return self.find(self.error_text_dict[error_text_key]).text


