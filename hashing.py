from passlib.context import CryptContext

class Hash:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password, hashed_password):
        return Hash.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(password):
        return Hash.pwd_context.hash(password)
