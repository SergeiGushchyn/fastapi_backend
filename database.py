from fastapi import HTTPException
import psycopg2
import psycopg2.extras
from internal.environment import dbc

def get_connection_and_cursor():
   try:
      conn = psycopg2.connect(dbc)
      cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
      return conn, cur
   except:
      raise HTTPException(status_code=500, detail="Database Error")