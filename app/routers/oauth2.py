from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import schema, Database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_Schema = OAuth2PasswordBearer(tokenUrl="login")

# Secret Key
# Algorithm
# Expiration Time

SECRET_KEY = "e2bae742d67b31027d9313a4b7a40b320ef682222ddc80e3c82e1cc0ef0e4ea65eee5bcccfbf7965e1b957f8039b3f184a75407bfef9a8ff58fae61bdd2111de4c95d6e600b82285a0333edd7382d479"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 60

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