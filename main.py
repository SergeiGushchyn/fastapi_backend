from fastapi import FastAPI
from google.oauth2 import service_account
import gspread
import json

from routers import authentication
from routers.api import records

app = FastAPI()
app.include_router(authentication.router)
app.include_router(records.router)

@app.get("/")
async def root():
   return {"message": "This is root"}
