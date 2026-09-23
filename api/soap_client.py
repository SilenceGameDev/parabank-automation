from zeep import Client
from logger import logger

WSDL = "https://parabank.parasoft.com/parabank/services/ParaBank?wsdl"

class ParaBankSOAP:
    def __init__(self):
        self.client = Client(WSDL)

    def get_account(self, account_id):
        logger.info(f"SOAP getAccount({account_id})")
        return self.client.service.getAccount(int(account_id))