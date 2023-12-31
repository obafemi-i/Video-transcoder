from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Depends
from fastapi.background import BackgroundTasks
from pymongo import MongoClient
from dotenv import dotenv_values
from redis_om import get_redis_connection

import gridfs
from contextlib import asynccontextmanager

from auth.access import get_current_user, router


config = dotenv_values()

redis_connect = get_redis_connection(
    host=config['HOST'],
    port=config['PORT'],
    password=config['PASSWORD'],
    decode_responses=True
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # app start
    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print('Connected to mongodb database.')

    yield

    # app close
    app.mongodb_client.close()
    print('Connection closed.')


app = FastAPI(lifespan=lifespan)
# app = FastAPI()
app.include_router(router)


@app.post('/upload')
async def upload_file(request: Request, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='No file provided.')
    

    fs = gridfs.GridFS(app.database)

    try:
        file_id = await fs.put(file)
        print(file_id)
        # print(await fs.get(file_id))

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Something went wrong, please try again.')
    
    queue_message = {
        'Video id': str(file_id),
        'Mp3 id': None,
        'User': current_user
    }

    redis_connect.xadd('video upload', queue_message, '*')

    return {'Message': f'Upload by {current_user} succesful.'}
