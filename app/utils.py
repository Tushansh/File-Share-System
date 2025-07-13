from passlib.context import CryptContext
from jose import jwt, JWTError
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
fernet = Fernet(Fernet.generate_key())

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def encrypt_id(id: int) -> str:
    return fernet.encrypt(str(id).encode()).decode()

def decrypt_id(token: str) -> int:
    return int(fernet.decrypt(token.encode()).decode())
