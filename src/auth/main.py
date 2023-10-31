from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# from .models import Base, User
import models
# from .database import engine, SessionLocal
import database
# from .schema import UserSchema, UserResponse
import schema
# from .hashing import get_password_hash, verify_password
import hashing
# from routes import user
# from .jwt_tokens import create_access_token
import jwt_tokens
# from .oauth import get_current_user
import oauth
# from typing import List


app = FastAPI()

# app.include_router(user.router)

database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.get('/')
def home():
    return {'message': 'welcome home'}


@app.post('/user')
def create_user(request: schema.UserSchema, db: Session= Depends(get_db)):
    hashed_password = hashing.get_password_hash(request.password)
    user = models.User(email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {'message': 'Account creation succesful!'}


@app.get('/user', response_model=list[schema.UserResponse])
def get_users(db: Session= Depends(get_db), current_user: schema.UserSchema = Depends(oauth.get_current_user)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}', response_model=schema.UserResponse)
def get_user(id: int, db: Session= Depends(get_db), current_user: schema.UserSchema = Depends(oauth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='No user with such ID')
    return user


@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Invalid login details')
    
    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Invalid login details')
    
    
    access_token = jwt_tokens.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    
    
