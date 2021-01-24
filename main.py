from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

DATABASE_URL = os.environ['DATABASE_URL']

@app.get("/")
async def root():
    return {"message": "Hello World"}
