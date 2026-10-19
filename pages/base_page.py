from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from logger import logger

DEFAULT_TIMEOUT_TIME = 10
PAGE_LOAD_TIMEOUT = 30

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # times out the webpage after 10s so no need to worry about wait.until() waiting forever in child classes
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT_TIME)
        self.page_timeout = PAGE_LOAD_TIMEOUT

    # def find(self, locator):
    #     return self.wait.until(EC.visibility_of_element_located(locator))

    def find(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        logger.info(f"Clicking {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        logger.info(f"Typing into {locator}")
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def select_by_index(self, locator, index: int):
        logger.info(f"Selecting option index {index} at {locator}")
        self.wait.until(
            lambda d: len(Select(d.find_element(*locator)).options) > 0
        )
        dropdown = Select(self.find(locator))
        dropdown.select_by_index(index)

    def get_option_values(self, locator) -> list:
        self.wait.until(lambda d: len(Select(d.find_element(*locator)).options) > 0)
        dropdown = Select(self.find(locator))
        return [opt.get_attribute("value") for opt in dropdown.options]

    def get_option_index_by_value(self, locator, value: str) -> int:
        values = self.get_option_values(locator)
        for i, v in enumerate(values):
            if v == str(value):
                return i
        raise ValueError(f"No option with value {value!r} found in dropdown {locator}")

    def get_last_account_option_value(self, locator) -> str:
        return self.get_option_values(locator)[-1]