from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users
from app.core.db import create_db_and_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
