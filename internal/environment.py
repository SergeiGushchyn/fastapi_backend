from dotenv import dotenv_values
import os

creds = ''
dbc = ''

if os.getenv('IS_PRODUCTION'):
   creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
   dbc = os.getenv('DATABASE_URL')
else:
   creds = dotenv_values(".env")['GOOGLE_APPLICATION_CREDENTIALS']
   dbc = dotenv_values(".env")['DATABASE_URL']