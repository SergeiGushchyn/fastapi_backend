from fastapi import FastAPI
from google.oauth2 import service_account
import gspread
import json

from routers import authentication

app = FastAPI()
app.include_router(authentication.router)
# async def get_records():
#    json_str = config
#    json_data = json.loads(json_str)
#    json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
#    scope = ['https://spreadsheets.google.com/feeds',
#                'https://www.googleapis.com/auth/drive']
#    credentials = service_account.Credentials.from_service_account_info(json_data, scopes=scope)
#    gc = gspread.authorize(credentials)
#    work_sheet = gc.open("Testing API").sheet1
#    return work_sheet


@app.get("/")
async def root():
   return {"message": "This is root"}
