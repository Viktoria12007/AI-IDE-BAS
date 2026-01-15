from sqlmodel import Session
from app.core.db import get_session
from typing import Annotated
from fastapi import Depends
from pwdlib import PasswordHash

SessionDep = Annotated[Session, Depends(get_session)]

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)
