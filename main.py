from fastapi import FastAPI
from google.oauth2 import credentials
import gspread
import os
import json

app = FastAPI()

async def get_records():
   json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
   # json_data = json.loads(json_str)
   # json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
   scope = ['https://spreadsheets.google.com/feeds',
               'https://www.googleapis.com/auth/drive']
   cred = credentials.Credentials.from_authorized_user_info(json_str, scope)
   gc = gspread.authorize(credentials)
   work_sheet = await gc.open("Testing API").sheet1
   return work_sheet


@app.get("/")
async def dashboard():
   ws = await get_records()
   return {"message": "Hello New York", "ws": ws}
