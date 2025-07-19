from fastapi import FastAPI
from src.controllers import bank, auth
from contextlib import asynccontextmanager
from src.database import database, metadata, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.account import account 
    from src.models.transaction import transaction
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()
    
tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication"
    },
    {
        "name": "bank",
        "description": "Operations for DIO Bank features"
    }
]

app = FastAPI(lifespan=lifespan,
              title="DIO Bank API",
              openapi_tags=tags_metadata,
              summary="API for DIO Bank features",
              description="""
## DIO Bank API Features:
You will be able to:

* **Create Account**.
* **Read Accounts**.        
* **Read Accounts by ID**.  
* **Create Transactions**.  
* **Read Transactions by ID**.        
              """)

app.include_router(auth.router)
app.include_router(bank.router, tags=["bank"])