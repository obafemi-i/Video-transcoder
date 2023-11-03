from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from jose import jwt, ExpiredSignatureError, JWTError
from dotenv import load_dotenv

router = APIRouter()
config = load_dotenv()

# Secret key to sign and verify JWT tokens
SECRET_KEY = config['SECRET_KEY']
ALGORITHM = "HS256"
AUTH_SERVICE_URL = config['AUTH_SERVICE_URL'] 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Function to get the current user from the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")



@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    # This endpoint will request authentication from the authentication service and return a token
    payload = {'username': request.username, 'password': request.password}

    response = requests.post(AUTH_SERVICE_URL, payload)
    
    if response.status_code == 200:
        token = response.json().get("access_token")

        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
