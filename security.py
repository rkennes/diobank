import time
from typing import Annotated
from uuid import uuid4

import jwt 
from fastapi import HTTPException, Request, status, Depends, Security 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel 

SECRET = "diobank"
ALGORITMH = "HS256"

security = HTTPBearer()

class AccessToken(BaseModel): 
    iss: str
    sub: int 
    aud: str
    exp: float
    iat: float 
    nbf: float
    jti: str

class JWTToken(BaseModel): 
    access_token: AccessToken 
    
def sign_jwt(user_id: int) -> dict: 
    now = time.time()
    
    payload = { 
        "iss": "diobank.com.br",
        "sub": str(user_id), 
        "aud": "diobank",
        "exp": now + (60 * 30),
        "iat": now, 
        "nbf": now,
        "jti": uuid4().hex,
    }
    
    token = jwt.encode(payload, SECRET, algorithm=ALGORITMH)
    return {"access_token": token}
    

async def decode_jwt(token: str) -> JWTToken | None: 
    try:
        decoded_token = jwt.decode(token, SECRET, audience="diobank", algorithms=[ALGORITMH])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        return _token if _token.access_token.exp >= time.time() else None 
    except Exception as e:
        return None 
    
class JWTBearer(HTTPBearer): 
    def __init__(self, auto_error:bool = True): 
        super(JWTBearer, self).__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> JWTToken: 
        
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")    
        
        if credentials: 
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid authorization scheme.")
            
            payload = await decode_jwt(credentials)
    
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token.")
            
            return payload
        else: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid authorization code.")

async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    jwt_token = await decode_jwt(token.credentials)

    if jwt_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )

    return {"user_id": jwt_token.access_token.sub}      
        

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")
    return current_user
