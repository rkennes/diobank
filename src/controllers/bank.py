from fastapi import  status, APIRouter, Depends
from src.schemas.bank import accountIn, transactionIn
from src.views.bank import accountOut, transactionOut
from src.models.account import account 
from src.models.transaction import transaction
from src.database import database
from src.services.bank import BankService
from security import login_required

router = APIRouter(prefix="/bank", dependencies=[Depends(login_required)])

service = BankService()

# routers
# post - create_account      - ok
# get  - read_accounts       - ok
# get  - read_account_by_id  - ok
# post - create_transaction  - ok
# get  - read_transactions   - 

@router.post("/create_account", status_code=status.HTTP_201_CREATED, response_model=accountOut)
async def create_account(data: accountIn):
    return await service.create_account(data)

@router.get("/read_accounts", response_model=list[accountOut])
async def read_accounts(limit: int, skip: int = 0):
    return await service.read_accounts(limit, skip)

@router.get("/read_account/{account_id}", response_model=accountOut)
async def read_account_by_id(account_id: int):
    return await service.read_account_by_id(account_id)

@router.post("/create_transaction/{account_id}", status_code=status.HTTP_201_CREATED, response_model=transactionOut)
async def create_transaction(account_id: int, data: transactionIn):
    return await service.create_transaction(account_id, data)

@router.get("/read_transactions/{account_id}", response_model=list[transactionOut])
async def read_transactions(account_id: int):
    return await service.read_transactions(account_id)                               