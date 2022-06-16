from fastapi import FastAPI, Request, Response, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from database import users
from passlib.context import CryptContext
from fastapi_login import LoginManager
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uvicorn

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRES_MINUTES = 60

manager = LoginManager(secret=SECRET_KEY,token_url="/", use_cookie=True)
manager.cookie_name = "auth"

@manager.user_loader()
def get_user_from_db(username: str):
    if username in users.keys():
        return UserDB(**users[username])

def authenticate_user(username: str, password: str):
    user = get_user_from_db(username=username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user

pwd_ctx = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password,hashed_password)


class User(BaseModel):
    username: str
 


class UserDB(User):
    hashed_password: str


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def get_home(request: Request):
#     return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "FriendConnect - Login"})

@app.post("/")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        return {"action":False}
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    # access_token = manager.create_access_token(
    #     data={"sub": user.username},
    #     expires=access_token_expires
    # )
    # resp = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    resp = {"action":True}
    # manager.set_cookie(resp,access_token)
    return resp
    

class NotAuthenticatedException(Exception):
    pass

def not_authenticated_exception_handler(request, exception):
    return RedirectResponse("/login")

manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

@app.get("/home")
def home(request: Request, user: User = Depends(manager)):
    user = User(**dict(user))
    return templates.TemplateResponse("home.html", {"request": request, "title": "FriendConnect - Home", "user": user})


# @app.get("/login", response_class=HTMLResponse)
# async def get_login(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "title": "FriendConnect - Login"})

# @app.post("/login")
# def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(username=form_data.username, password=form_data.password)
#     if not user:
#         return templates.TemplateResponse("login.html", {"request": request, "title": "FriendConnect - Login", "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
#     access_token = manager.create_access_token(
#         data={"sub": user.username},
#         expires=access_token_expires
#     )
#     resp = RedirectResponse("/home", status_code=status.HTTP_302_FOUND)
#     manager.set_cookie(resp,access_token)
#     return resp

# class NotAuthenticatedException(Exception):
#     pass

# def not_authenticated_exception_handler(request, exception):
#     return RedirectResponse("/login")

# manager.not_authenticated_exception = NotAuthenticatedException
# app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

# @app.get("/home")
# def home(request: Request, user: User = Depends(manager)):
#     user = User(**dict(user))
#     return templates.TemplateResponse("home.html", {"request": request, "title": "FriendConnect - Home", "user": user})

if __name__=="__main__":
    uvicorn.run(app,debug = True)
