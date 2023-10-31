from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from contextlib import asynccontextmanager


config = dotenv_values()
# print(config['ATLAS_URI'])
# uri = "mongodb+srv://Obafemi:obafemi@cluster1.esmjidp.mongodb.net/?retryWrites=true&w=majority"

# print('uri', uri)

# if config['ATLAS_URI'] == uri:
#     print(True)

def start_db():
    try:
        mongodb_client = MongoClient(config["ATLAS"])
        print('Connected to mongodb database!')
        database = mongodb_client[config['DB_NAME']]
        
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


