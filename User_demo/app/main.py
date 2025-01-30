from typing import Any

from fastapi import FastAPI, Depends, HTTPException
from . import models
from .database import engine
from .dependencies import get_db
from .crud.user import create_user,login_user
from .crud.message import store_message,get_all_message
from .schemas.user import UserCreate, User, Login, UserBase
from .schemas.message import MessageCreate, Messege_get, MessageResponse
from sqlalchemy.orm import Session

# Uncomment the following line if you need to create the tables manually when the app starts.
# models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # List of allowed origins (React app)
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allowed methods
    allow_headers=["Content-Type", "Authorization"],  # Allowed headers
)

@app.get("/")
def get_h():
    return "App is running"

@app.post("/users/")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) :
     msg=  create_user(db=db, user=user)
     return msg


@app.post("/login")
def login(login_data: Login, db: Session = Depends(get_db)):  # Use Login schema here
    login_result = login_user(db=db, mobile=login_data.mobile, password=login_data.password)
    return login_result

@app.post("/MessageCreate")
def Message(mesg:MessageCreate,db:Session=Depends(get_db)):
    msgs= store_message(db=db,message=mesg)
    return msgs

@app.get("/message/{user_id}", response_model=list[MessageResponse])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    # Call the get_all_message function passing the user_id to get the messages for that user
    message_data = get_all_message(db=db, message=Messege_get(user_id=user_id))
    return message_data