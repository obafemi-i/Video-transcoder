from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schema import UserSchema, UserResponse
from ..hashing import get_password_hash
from ..models import User
from ..database import SessionLocal

router = APIRouter(prefix='/account', tags=['Account'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
def create_user(request: UserSchema, db: Session= Depends(get_db)):
    hashed_password = get_password_hash(request.password)
    user = User(email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {'message': 'Account creation succesful!'}



@router.get('/user', response_model = UserResponse)
def get_users(db: Session= Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get('/user/{id}', response_model=UserResponse)
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user