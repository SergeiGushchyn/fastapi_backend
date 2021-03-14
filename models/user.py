from pydantic import BaseModel

class User(BaseModel):
   email: str
   first_name: str
   last_name: str

class Login(BaseModel):
   email: str
   password: str

class Register(BaseModel):
   email: str
   password: str
   first_name: str
   last_name: str