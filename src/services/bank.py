from src.database import database
from databases.interfaces import Record
from fastapi import HTTPException, status
from src.models.account import account
from src.models.transaction import transaction 
from src.schemas.bank import accountIn, transactionIn 
from datetime import datetime

class BankService: 
    async def read_accounts(self, limit: int, skip: int = 0) -> list[Record]:
        query = account.select().limit(limit).offset(skip)
        return await database.fetch_all(query) 
    
    async def read_account_by_id(self, id_account:int) -> Record: 
        return await self.__get_by_id_account(id_account) 
    
    async def create_account(self, data:accountIn) -> int:  
        created = data.created_at or datetime.now()
        
        command = account.insert().values(
            owner=data.owner, 
		    balance=data.balance, 
		    created_at=created, 
        ) 
        new_id = await database.execute(command) 
        return await self.__get_by_id_account(new_id)
        
    
    async def create_transaction(self, id_account:int, data:transactionIn) -> Record:  
        # validate id_account
        acc = await self.__get_by_id_account(id_account)  
        print(acc)
        
        if not acc:
            return
        
        type = data.type.lower() 
        value = data.value
        
        if type not in ["debt", "credit"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type invalid. Use Debt or Credit")

        if value <= 0: 
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Negative value. Operation not completed."
                )

        if type == "debt":
            if acc["balance"] < value:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient balance. Operation not completed."
                )
            new_balance = acc["balance"] - value
        else: 
            new_balance = acc["balance"] + value
        
        created = data.created_at or datetime.now()
        command = transaction.insert().values(
            id_account = id_account,
            type=data.type, 
		    value=data.value, 
		    created_at=created, 
        ) 
        new_id = await database.execute(command) 
        
        update_command = account.update().where(account.c.id_account == id_account).values(balance=new_balance)
        await database.execute(update_command)
        
        
        query = transaction.select().where(transaction.c.id_transaction == new_id)
        result = await database.fetch_one(query)

        if not result:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Transaction missing after insert.")

        return result
    
    async def read_transactions(self, id_account: int) -> list[dict]:
        query = transaction.select().where(transaction.c.id_account == id_account)
        results = await database.fetch_all(query)
        
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transactions not found with this account_id."
            )

        return [dict(row) for row in results]

    
    async def __get_by_id_account(self, id_account: int) -> Record: 
        query = account.select().where(account.c.id_account == id_account) 
        result = await database.fetch_one(query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account number not found.")
        return result