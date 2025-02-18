from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Todos
from database import SessionLocal
from routers.auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
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



@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user:user_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, user:user_dependency, todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
