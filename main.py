from fastapi import FastAPI
from google.oauth2 import service_account
import gspread
import os
import json

from dotenv import dotenv_values


if os.getenv('IS_PRODUCTION'):
   config = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
else:
   config = dotenv_values(".env")['GOOGLE_APPLICATION_CREDENTIALS']

# from internal import config

app = FastAPI()
# settings = config.Settings()

async def get_records():
   json_str = config
   json_data = json.loads(json_str)
   json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
   scope = ['https://spreadsheets.google.com/feeds',
               'https://www.googleapis.com/auth/drive']
   credentials = service_account.Credentials.from_service_account_info(json_data, scopes=scope)
   gc = gspread.authorize(credentials)
   work_sheet = gc.open("Testing API").sheet1
   return work_sheet


@app.get("/")
async def dashboard():
   ws = await get_records()
   return {"message": "Hello New York", "ws": ws.row_values(2)}
