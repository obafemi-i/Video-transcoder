from fastapi import FastAPI, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
from jose import jwt, ExpiredSignatureError, JWTError


app = FastAPI()

# Secret key to sign and verify JWT tokens
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
AUTH_SERVICE_URL = "http://127.0.0.1:8080/login"  # Change this to the URL of your authentication service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
    

def get_current_user(token: str = Depends(oauth2_scheme)):
# def get_current_user(token: str = get_token_from_form):
    # Function to get the current user from the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # email: str = payload.get("sub")
        print(payload)
        return payload.get('sub')
        # token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@app.get("/secure-endpoint")
def secure_endpoint(current_user: dict = Depends(get_current_user)):
    # Your secure endpoint logic goes here
    return {"message": "This is a secure endpoint", "user": current_user}


@app.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends()):
    # This endpoint will request authentication from the authentication service and return a token
    payload = {'username': request.username, 'password': request.password}

    response = requests.post(AUTH_SERVICE_URL, payload)
    
    if response.status_code == 200:
        token = response.json().get("access_token")

        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
