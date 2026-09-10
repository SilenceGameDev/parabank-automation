from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import logger

DEFAULT_TIMEOUT_TIME = 10

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # times out at the webpage after 10s so no need to worry about wait.until waiting forever in child classes
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT_TIME)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        logger.info(f"Clicking {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        logger.info(f"Typing into {locator}")
        el = self.find(locator)
        el.clear()
        el.send_keys(text)