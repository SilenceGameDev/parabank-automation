import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield drv
    drv.quit()

@pytest.fixture
def known_account_id():
    # Log into ParaBank manually, check Accounts Overview, and use a real
    # account number from your dedicated test account here
    return "13344"  # replace with your actual account ID