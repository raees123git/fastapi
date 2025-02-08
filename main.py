from fastapi import FastAPI, Request, status
from models import Base
from database import engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# print(models.check)
app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='To_Do_App/templates')
app.mount('/static', StaticFiles(directory='To_Do_App/static'), name='static')



@app.get('/')
def test(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)


# endpoint to check wether or app is running correctly or not
@app.get('/healthy')
def health_check():
    return {'status': 'healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
