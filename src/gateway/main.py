from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Depends
from fastapi.background import BackgroundTasks
from pymongo import MongoClient
from dotenv import dotenv_values
import pika
import requests
from redis_om import get_redis_connection

import gridfs
from contextlib import asynccontextmanager

from schema import Login
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError

config = dotenv_values()

redis_connect = get_redis_connection(
    host=config['HOST'],
    port=config['PORT'],
    password=config['PASSWORD'],
    decode_responses=True
)

def start_db():
    try:
        mongodb_client = MongoClient(config['ATLAS_URI'])
        print('Connected to mongodb database!')
        database = mongodb_client[config['DB_NAME']]
        fs = gridfs.GridFS(database)
        return fs

    except Exception as e:
        print(e)


def close_db():
    mongodb_client = MongoClient(config['ATLAS_URI'])
    mongodb_client.close()
    print('connection closed')


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app start
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print('Connected to mongodb database!')

    yield

    # app close
    app.mongodb_client.close()
    print('Connection closed')


# app = FastAPI(lifespan=lifespan)
app = FastAPI()


# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='file_queue')
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Function to get the current user from the token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # email: str = payload.get("sub")
        return payload
        # token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    

@app.post('/access')
def get_access(request: Login):

    url = 'http://127.0.0.1:8080/login'

    data = request.username
    passw = request.password

    datad = {'username':data, 'password': passw}

    response = requests.post(url, data=datad)

    print('response', response.json()['access_token'])

    return response.json()


@app.post('/upload')
async def upload_file(request: Request,file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='No file provided.')
    
    fs = gridfs.GridFS(request.app.database)
    try:
        file_id = fs.put(file)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong, please try again.')
    
    queue_message = {
        'Video id': file_id,
        'Mp3 id': None
    }
    redis_connect.xadd('video upload', queue_message, '*')

    # print('reqqq',request.app.database)

