from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request
from pymongo import MongoClient
from dotenv import dotenv_values
import pika
import requests

import gridfs
from contextlib import asynccontextmanager

from schema import Login


config = dotenv_values()

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
    # start_db()
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print('Connected to mongodb database!')

    yield
    # close_db()

    app.mongodb_client.close()
    print('Connection closed')


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='file_queue')

@app.post('/access')
def get_access(request: Login):

    url = 'http://127.0.0.1:8000/login'

    data = request.username
    passw = request.password

    datad = {'username':data, 'password': passw}

    response = requests.post(url, data=datad)

    print('response', response.json()['access_token'])

    return response.json()

@app.post('/upload')
async def upload_file(request: Request,file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='No file provided')
    
    file_id = ''
    print('reqqq',app.database)