from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Todos, Users
from database import SessionLocal
from auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix='/users',
    tags=['users']
)


# print('i am chekinkdddddddddddd')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=2)


@router.get('/todo/info_user/')
def info_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_info = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_info


@router.put('/todo/change_password/')
def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


# route to update phone number
@router.put('/todo/change_phone_num/')
def change_phone_number(user: user_dependency, db: db_dependency, new_number: str | None = None):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = new_number
    db.add(user_model)
    db.commit()
