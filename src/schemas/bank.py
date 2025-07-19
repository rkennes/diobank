from datetime import datetime
from pydantic import BaseModel

class accountIn(BaseModel): 
    owner: str
    balance: float
    created_at: datetime | None = None

class transactionIn(BaseModel): 
    type: str 
    value: float
    created_at: datetime | None = None    