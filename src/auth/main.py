from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .models import Base, User
from .database import engine, SessionLocal
from .schema import UserSchema, UserResponse
from .hashing import get_password_hash, verify_password
# from routes import user
from .jwt import create_access_token
from .oauth import get_current_user
from typing import List, Optional, Annotated


app = FastAPI()

# app.include_router(user.router)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.get('/')
def home():
    return {'message': 'welcome home'}


@app.post('/user')
def create_user(request: UserSchema, db: Session= Depends(get_db)):
    hashed_password = get_password_hash(request.password)
    user = User(email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {'message': 'Account creation succesful!'}


@app.get('/user', response_model=List[UserResponse])
def get_users(db: Session= Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    users = db.query(User).all()
    return users


@app.get('/user/{id}', response_model=UserResponse)
def get_user(id: int, db: Session= Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='No user with such ID')
    return user


@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Invalid login details')
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Invalid login details')
    
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
    
    
