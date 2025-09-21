from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from CRUD.Routers import auth_token
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    return auth_token.verify_token(token)
