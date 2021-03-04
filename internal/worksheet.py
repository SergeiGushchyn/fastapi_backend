from google.oauth2 import service_account
from internal.environment import creds
import gspread
import json

async def get_worksheet():
   json_str = creds
   json_data = json.loads(json_str)
   json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')
   scope = ['https://spreadsheets.google.com/feeds',
               'https://www.googleapis.com/auth/drive']
   credentials = service_account.Credentials.from_service_account_info(json_data, scopes=scope)
   gc = gspread.authorize(credentials)
   work_sheet = gc.open("Testing API").sheet1
   return work_sheet