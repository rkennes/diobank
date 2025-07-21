from fastapi import status
from httpx import AsyncClient 

async def test_create_account_success(client: AsyncClient, access_token: str):
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"owner" : "automated test", "balance" : 1200.0}
    
    # When 
    response = await client.post("/bank/create_account", json=data, headers=headers)
    
    # Then 
    content = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id_account"] is not None 
    