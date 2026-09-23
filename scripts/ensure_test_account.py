from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from config import MY_TEST_USER
from logger import logger

def ensure_test_account_exists(driver):
    """Idempotent: logs in if the dedicated account already exists,
    registers it fresh if it doesn't (e.g. after a ParaBank reset)."""
    login = LoginPage(driver)
    login.load()
    try:
        login.login(MY_TEST_USER.username, MY_TEST_USER.password)
        logger.info(f"Test account '{MY_TEST_USER.username}' already exists — reusing it.")
    except TimeoutException:
        logger.info(f"Test account '{MY_TEST_USER.username}' not found — registering fresh.")
        register = RegisterPage(driver)
        register.register_user(MY_TEST_USER.username, MY_TEST_USER.password)