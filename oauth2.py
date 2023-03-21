from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from database import get_db
from tokens import Token
class OAuth2:

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    async def get_current_user(token: str = Depends(oauth2_scheme),db = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        user_id = Token.verify_token(token,credentials_exception)

        return user_id