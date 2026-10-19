from api.rest_client import ParaBankAPI
from api.schemas import AccountSchema
from api.soap_client import ParaBankSOAP
import pytest
from logger import logger

rest_api = ParaBankAPI()
soap_api = ParaBankSOAP()

def test_get_account_returns_200(known_account_id):
    resp = rest_api.get_account(known_account_id)
    assert resp.status_code == 200
    validated = AccountSchema(**resp.json())
    assert validated.id == int(known_account_id)
    assert validated.type in ("CHECKING", "SAVINGS")

@pytest.mark.parametrize("invalid_id,expected_status", [
    ("999999999", 400),  # valid format, nonexistent account
    ("-1", 400),          # valid format, invalid value
    ("abc", 404),          # non-numeric, fails differently
])
def test_get_account_invalid_id_returns_expected_status(invalid_id, expected_status):
    resp = rest_api.get_account(invalid_id)
    assert resp.status_code == expected_status, (
        f"Expected {expected_status} for ID {invalid_id!r}, got {resp.status_code}"
    )

def test_get_account_via_soap(known_account_id):
    result = soap_api.get_account(known_account_id)
    assert result is not None
    assert str(result.id) == str(known_account_id)


def test_soap_matches_rest_for_same_account(known_account_id):
    soap_result = soap_api.get_account(known_account_id)
    rest_result = rest_api.get_account(known_account_id).json()

    soap_balance = float(soap_result.balance)
    rest_balance = float(rest_result["balance"])

    logger.info(f"SOAP balance: {soap_balance}, REST balance: {rest_balance}")
    assert soap_balance == pytest.approx(rest_balance, abs=0.01)