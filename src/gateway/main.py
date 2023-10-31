from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
import pika

import gridfs
from contextlib import asynccontextmanager


config = dotenv_values()

def start_db():
    try:
        mongodb_client = MongoClient(config["ATLAS_URI"])
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
    start_db()

    yield

    close_db()


app = FastAPI(lifespan=lifespan)


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

