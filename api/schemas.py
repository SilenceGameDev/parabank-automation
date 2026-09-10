from pydantic import BaseModel

class AccountSchema(BaseModel):
    id: int
    customerId: int
    type: str
    balance: float