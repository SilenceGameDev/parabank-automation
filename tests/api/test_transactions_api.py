from api.rest_client import ParaBankAPI
from logger import logger

api = ParaBankAPI()

def test_get_transactions_returns_200(known_account_id):
    resp = api.get_transactions(known_account_id)
    assert resp.status_code == 200

def test_get_transactions_invalid_account_id():
    resp = api.get_transactions("999999999")
    logger.info(f"GET transactions for invalid ID returned status {resp.status_code}")
    assert resp.status_code == 400  # confirmed via manual run — matches accounts endpoint behavior