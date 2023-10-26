from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Base, User
from database import engine, SessionLocal
from schema import UserSchema, UserResponse
from hashing import get_password_hash
# from passlib.context import CryptContext

app = FastAPI()

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


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post('/user')
def create_user(request: UserSchema, db: Session= Depends(get_db)):
    hashed_password = get_password_hash(request.password)
    user = User(email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {'message': 'Account creation succesful!'}


@app.get('/user', response_model=UserResponse)
def get_users(db: Session= Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get('/user/{id}', response_model=UserResponse)
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user

