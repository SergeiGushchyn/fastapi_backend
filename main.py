from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import authentication
from routers.api import records

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(records.router)

@app.get("/")
async def root():
   return {"message": "This is root"}
