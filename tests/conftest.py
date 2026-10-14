import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from pathlib import Path
from models import User
from pages.login_page import LoginPage
from pages.accounts_overview_page import AccountsOverviewPage
from config import MY_TEST_USER
from scripts.ensure_test_account import ensure_test_account_exists
from scripts.setup_low_balance_account import create_low_balance_account, DRAIN_TARGET
from scripts.discover_account_id import discover_known_account_id
from scripts.generate_known_transaction import generate_known_transaction, TRANSFER_AMOUNT

def load_users():
    project_root = Path(__file__).resolve().parents[1]  # tests/ -> project root
    users_path = project_root / "test_data" / "users.json"
    with open(users_path) as f:
        raw = json.load(f)
    return {name: User(**data) for name, data in raw.items()}

@pytest.fixture
def users():
    return load_users()

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield drv
    drv.quit()

def make_temp_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Used to register an account once a session. Ensure .env is setup with ur account credentials
# Parabank does an account purge approx every day so having this here instead of re-registering that account manually everyday
@pytest.fixture(scope="session", autouse=True)
def setup_test_account():
    temp_driver = make_temp_driver()
    ensure_test_account_exists(temp_driver)
    temp_driver.quit()



@pytest.fixture(scope="session")
def known_account_id(setup_test_account):
    temp_driver = make_temp_driver()
    account_id = discover_known_account_id(temp_driver)
    temp_driver.quit()
    return account_id

# Used to quickly setup logging in for tests. Returns AccountsOverviewPage to navigate loading to the desired page.
@pytest.fixture
def logged_in_accounts_page(driver):
    login = LoginPage(driver)
    login.load()
    login.login(MY_TEST_USER.username, MY_TEST_USER.password)
    return AccountsOverviewPage(driver)

@pytest.fixture(scope="session")
def low_balance_account(setup_test_account):
    temp_driver = make_temp_driver()
    account_id = create_low_balance_account(temp_driver)
    temp_driver.quit()
    return {"account_id": account_id, "balance": DRAIN_TARGET}

@pytest.fixture(scope="session")
def known_transaction(known_account_id):
    temp_driver = make_temp_driver()
    transaction = generate_known_transaction(temp_driver, known_account_id)
    temp_driver.quit()
    return transaction

# test template
# def test_x(driver, logged_in_accounts_page):
#     logged_in_accounts_page.load_<whichever>_page()
#
#     page = <WhicheverPage>(driver)
#     page.<do the actual thing>()             # page-specific action only
#     assert "something about the result"