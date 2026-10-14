from pages.login_page import LoginPage
from config import MY_TEST_USER, TEST_FIRST_NAME, TEST_LAST_NAME


def test_valid_login_shared_demo(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["shared_demo_user"]
    login.login(creds.username, creds.password)
    assert creds.username in login.get_welcome_text()

def test_valid_login_dedicated_account(driver):
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)
    welcome = login.get_welcome_text()
    assert f"{TEST_FIRST_NAME} {TEST_LAST_NAME}".lower() in welcome.lower()

def test_invalid_login_shows_error(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["invalid_password"]
    login.login_expecting_error(creds.username, creds.password)
    assert "error" in login.get_error_text()