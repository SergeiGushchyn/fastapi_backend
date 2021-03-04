from dotenv import dotenv_values
import os

creds = ''
dbc = ''
secret = ''
alg = ''

if os.getenv('IS_PRODUCTION'):
   creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
   dbc = os.getenv('DATABASE_URL')
   secret = os.getenv('SECRET')
   alg = os.getenv('ALGORITHM')
else:
   creds = dotenv_values(".env")['GOOGLE_APPLICATION_CREDENTIALS']
   dbc = dotenv_values(".env")['DATABASE_URL']
   secret = dotenv_values(".env")['SECRET']
   alg = dotenv_values(".env")['ALGORITHM']