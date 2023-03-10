from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from tokens import Token
from operations.user_ops import UserOps
class OAuth2:

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        email = Token.verify_token(token,credentials_exception)

        return UserOps.get_by_email(email)
        