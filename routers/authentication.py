from fastapi import Form, APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from pydantic import parse_obj_as
from datetime import datetime, timedelta

from database import get_connection_and_cursor
from internal.errors import authentication_errors
from models.user import User, Login, Register
from internal.environment import secret, alg

TOKEN_EXP_MIN = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def create_token(data: dict, expires_delta: timedelta):
   to_encode = data.copy()
   expire = datetime.utcnow() + expires_delta
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, secret, algorithm=alg)
   return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   try:
      payload = jwt.decode(token, secret, algorithms=[alg])
      email: str = payload.get("sub")
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
      if email is None:
         raise credentials_exception
   except JWTError:
      raise credentials_exception

@router.post("/register")
async def register_user(register: Register):
   conn, cur = get_connection_and_cursor()
   cur.execute("""
      insert into users (email, hashed_password, first_name, last_name)
      values(%s, crypt(%s, gen_salt(%s)), %s, %s);
      """,
      (register.email, register.password, 'bf', register.first_name, register.last_name))
   conn.commit()
   cur.close()
   conn.close()
   return "Worked"

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
   if not user:
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Incorrect username or password",
         headers={"WWW-Authenticate": "Bearer"},
      )
   access_token_expires = timedelta(minutes=TOKEN_EXP_MIN)
   access_token = create_token(
      data={"sub": user.email}, expires_delta=access_token_expires
   )
   cur.close()
   conn.close()
   return {"access_token": access_token, "token_type": "bearer"}
