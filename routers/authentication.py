from fastapi import Form, APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from pydantic import parse_obj_as
from datetime import datetime, timedelta

from database import get_connection_and_cursor
from models.user import User, Login, Register
from internal.environment import secret, alg

import psycopg2

TOKEN_EXP_MIN = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def create_token(data: dict):
   access_token_expires = timedelta(minutes=TOKEN_EXP_MIN)
   to_encode = data.copy()
   expire = datetime.utcnow() + access_token_expires
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, secret, algorithm=alg)
   return {"access_token": encoded_jwt, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   try:
      payload = jwt.decode(token, secret, algorithms=[alg])
      email: str = payload.get("sub")
      if email is None:
         raise credentials_exception
      conn, cur = get_connection_and_cursor()
      cur.execute("""
      select email, first_name, last_name from users
      where email = %s;
      """,
      [email])
      user = User(**cur.fetchone())
      if user is None:
         raise credentials_exception
      return user
   except JWTError:
      raise credentials_exception
   finally:
      conn.close()
      cur.close()

@router.get("/user")
async def get_user(user = User(Depends(get_current_user))):
   if user is not None:
      return user


@router.post("/register")
async def register_user(register: Register):
   try:
      conn, cur = get_connection_and_cursor()
      cur.execute("""
      insert into users (email, hashed_password, first_name, last_name)
      values(%s, crypt(%s, gen_salt(%s)), %s, %s);
      """,
      (register.email, register.password, 'bf', register.first_name, register.last_name))
      conn.commit()
      access_token = create_token({"sub": register.email})
      return access_token
   except psycopg2.Error as e:
      raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=e.diag.message_detail.partition("=")[2],
      headers={"WWW-Authenticate": "Bearer"},
   )
   finally:
      cur.close()
      conn.close()

@router.post("/login")
async def login_user(login: Login):
   conn, cur = get_connection_and_cursor()   
   cur.execute("""
      select email, first_name, last_name from users
      where email = %s
      and hashed_password = crypt(%s, hashed_password);
      """,
      (login.email, login.password))
   user = User(**cur.fetchone())
   cur.close()
   conn.close()
   if not user:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Incorrect username or password",
         headers={"WWW-Authenticate": "Bearer"},
      )
   access_token = create_token({"sub": user.email})
   return access_token
