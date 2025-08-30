 
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: UserCreate) -> User:
        
        existing_user = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise ValueError("Username already registered")
        
        
        hashed_password = get_password_hash(user_data.password)
        user = User(username=user_data.username, password_hash=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user