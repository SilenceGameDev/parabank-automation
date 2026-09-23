from pages.login_page import LoginPage
from config import MY_TEST_USER

def test_valid_login_shared_demo(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["shared_demo_user"]
    login.login(creds.username, creds.password)
    assert "overview.htm" in driver.current_url

def test_valid_login_dedicated_account(driver):
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)
    assert "overview.htm" in driver.current_url

def test_invalid_login_shows_error(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["invalid_password"]
    login.login_expecting_error(creds.username, creds.password)
    assert "error" in login.get_error_text()