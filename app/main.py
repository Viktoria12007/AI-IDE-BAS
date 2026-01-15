from fastapi import FastAPI
from .routers import users
from app.core.db import create_db_and_tables

app = FastAPI()

app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
