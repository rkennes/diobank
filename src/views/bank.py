from datetime import datetime
from pydantic import BaseModel

class accountOut(BaseModel): 
    id_account: int
    owner: str
    balance: float
    created_at: datetime | None = None

class transactionOut(BaseModel): 
    id_transaction : int
    id_account: int
    type: str 
    value: float
    created_at: datetime | None = None    