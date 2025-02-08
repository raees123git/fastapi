from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory='To_Do_App/templates')
router = APIRouter(
    prefix='/todos',
    tags=['todos']

)


# print('i am chekinkdddddddddddd')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The Session type ensures that the object you’re working with is an SQLAlchemy session.
# It makes it clear to anyone reading the code that this dependency (db_dependency) is tied to an SQLAlchemy session.
db_dependency = Annotated[Session, Depends(get_db)]

# This line is defining db_dependency, which:
#
# Uses Depends(get_db) → This tells FastAPI to run the get_db() function to obtain a database session (SessionLocal()).
# Uses Annotated[Session, ...] → This is just type hinting to indicate that db_dependency is a SQLAlchemy Session.
# How It Works
# Every time a route function is called, FastAPI automatically calls get_db(), providing a fresh database session (db).
# Once the route function is done, FastAPI closes the session.


user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


###### pages

@router.get('/todo-page')
async def render_todo_page(db: db_dependency, request: Request):
    print('i am hereeeeeeeeeeeeeeeeeeeeeeeee')
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            print('no userrrrrrrrrrrrrrrrrrrrrrrrrr')
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

        return templates.TemplateResponse('todo.html', {"request": request, 'todos': todos, 'user': user})

    except Exception as e:

        print(f"Error occurred: {e}")  # Replace with proper logging in production

        return redirect_to_login()

@router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


    except Exception as e:

        print(f"Error occurred: {e}")  # Replace with proper logging in production

        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


    except Exception as e:

        print(f"Error occurred: {e}")  # Replace with proper logging in production

        return redirect_to_login()


# ####### Endpoints
@router.get('/')
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')


# db: db_dependency is used in FastAPI route functions to inject a database session.
@router.post('/todo')
def create_book(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        print('ioooooooooooooooooooooooooooooooo')
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}')
def update_todo(user: user_dependency, db: db_dependency,
                todo_request: TodoRequest,
                todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete('/todo/{todo_id}')
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
