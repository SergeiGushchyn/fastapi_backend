from fastapi import HTTPException
import psycopg2
from internal.environment import dbc

def get_connection_and_cursor():
   try:
      conn = psycopg2.connect(dbc)
      cur = conn.cursor()
      return conn, cur
   except:
      raise HTTPException(status_code=500, detail="Database Error")