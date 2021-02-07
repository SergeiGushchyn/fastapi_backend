from fastapi import FastAPI, Form, APIRouter, HTTPException
from database import get_connection_and_cursor
from internal.errors import authentication_errors

router = APIRouter()

def validate_not_empty(email: str, password: str):
   if email is None or password is None:
      raise HTTPException(status_code=400, detail=authentication_errors["EMPTY"])

@router.post("/register")
async def register_user(email: str = Form(...), password: str = Form(...)):
   validate_not_empty(email, password)
   conn, cur = get_connection_and_cursor()
   cur.execute("""
      insert into users (email, hashed_password)
      values(%s, crypt(%s, gen_salt(%s)));
      """,
      (email, password, 'bf'))
   conn.commit()
   cur.close()
   conn.close()

@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
   validate_not_empty(email, password)
   conn, cur = get_connection_and_cursor()
   cur.execute("""
      select user_id from users
      where email = %s
      and hashed_password = crypt(%s, hashed_password);
      """,
      (email, password))
   id = cur.fetchone()
   if id is None:
      raise HTTPException(status_code=404, detail=authentication_errors["INCORRECT"])
   cur.close()
   conn.close()
   return {"user": id[0]}
