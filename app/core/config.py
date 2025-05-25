from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os

DATABASE_URL = "sqlite:///./app/database.db"

SECRET_KEY = "aosidj342390AOKPLSDopk2390$@()2ji1[app-0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

SERVER_URL = "http://localhost:8000"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
