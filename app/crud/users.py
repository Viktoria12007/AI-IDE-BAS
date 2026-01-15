from sqlalchemy.exc import IntegrityError
from fastapi import Query, HTTPException, status
from app.models.users import UserCreate, User, UserUpdate
from app.dependencies import SessionDep, get_password_hash
from sqlmodel import select
from typing import Annotated


def r_create_user(user: UserCreate, session: SessionDep):
    db_user = User(**user.model_dump())
    try:
        db_user.password = get_password_hash(db_user.password)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed: user.email" in str(e):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already exists")
        elif "UNIQUE constraint failed: user.username" in str(e):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already exists")
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect data was passed when creating a user")


def r_read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


def r_read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user


def r_update_user(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = r_read_user(user_id, session)
    try:
        if user.password:
            user.password = get_password_hash(user.password)
        user_data = user.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(user_data)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed: user.email" in str(e):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already exists")
        elif "UNIQUE constraint failed: user.username" in str(e):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already exists")
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect data was passed when updating a user")


def r_delete_user(user_id: int, session: SessionDep):
    user = r_read_user(user_id, session)
    session.delete(user)
    session.commit()
    return {"ok": True}
