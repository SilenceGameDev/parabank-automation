from api.rest_client import ParaBankAPI
from api.schemas import AccountSchema
import pytest

api = ParaBankAPI()

def test_get_account_returns_200(known_account_id):
    resp = api.get_account(known_account_id)
    assert resp.status_code == 200
    validated = AccountSchema(**resp.json())
    assert validated.balance >= 0

@pytest.mark.parametrize("invalid_id,expected_status", [
    ("999999999", 400),  # valid format, nonexistent account
    ("-1", 400),          # valid format, invalid value
    ("abc", 404),          # non-numeric, fails differently
])
def test_get_account_invalid_id_returns_expected_status(invalid_id, expected_status):
    resp = api.get_account(invalid_id)
    assert resp.status_code == expected_status, (
        f"Expected {expected_status} for ID {invalid_id!r}, got {resp.status_code}"
    )