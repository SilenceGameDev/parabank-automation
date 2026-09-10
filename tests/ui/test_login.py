import pytest
import json
from pages.login_page import LoginPage
from config import MY_TEST_USER
from pathlib import Path

def load_users():
    # tests/ui/test_login.py -> go up two levels to reach the project root
    project_root = Path(__file__).resolve().parents[2]
    users_path = project_root / "test_data" / "users.json"
    with open(users_path) as f:
        return json.load(f)

@pytest.fixture
def users():
    return load_users()

def test_valid_login_dedicated_account(driver):
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)
    assert "overview.htm" in driver.current_url

def test_valid_login_shared_demo(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["shared_demo_user"]
    login.login(creds["username"], creds["password"])
    assert "overview.htm" in driver.current_url

def test_invalid_login_shows_error(driver, users):
    login = LoginPage(driver)
    login.load()
    creds = users["invalid_password"]
    login.login(creds["username"], creds["password"])
    assert "overview.htm" in driver.current_url