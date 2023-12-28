from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schema, Database, models, utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: schema.UserLogin, db: Session = Depends(Database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentails"
            )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentails"
        )

    return {"test", "credentails matched"}