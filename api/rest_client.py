# api/rest_client.py
import requests

BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

class ParaBankAPI:
    def get_account(self, account_id):
        return requests.get(f"{BASE_URL}/accounts/{account_id}",
                             headers={"Accept": "application/json"})

    def get_transactions(self, account_id):
        return requests.get(f"{BASE_URL}/accounts/{account_id}/transactions",
                             headers={"Accept": "application/json"})