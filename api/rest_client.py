import requests
from logger import logger

BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

class ParaBankAPI:
    def get_account(self, account_id):
        url = f"{BASE_URL}/accounts/{account_id}"
        response = requests.get(url, headers={"Accept": "application/json"})
        logger.info(f"GET {url} -> {response.status_code}")
        return response

    def get_transactions(self, account_id):
        url = f"{BASE_URL}/accounts/{account_id}/transactions"
        response = requests.get(url, headers={"Accept": "application/json"})
        logger.info(f"GET {url} -> {response.status_code}")
        return response