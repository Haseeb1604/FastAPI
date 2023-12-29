from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import schema, Database, models
from ..config import settings
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_Schema = OAuth2PasswordBearer(tokenUrl="login")

# Secret Key
# Algorithm
# Expiration Time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRES_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentails_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentails_exception

        token_data = schema.TokenData()
        token_data.id = id
    except JWTError:
        raise credentails_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_Schema), db: Session = Depends(Database.get_db)):
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could Not Validiate credentials",
        headers={"WWW-Authenticate": "Bearer"}
        )
    token_id = verify_access_token(token, credentails_exception)
    user = db.query(models.User).filter(models.User.id == token_id.id).first()
    return user