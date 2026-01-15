from fastapi import APIRouter, Query, status
from typing import Annotated
from app.models.users import UserCreate, UserPublic, UserUpdate
from app.dependencies import SessionDep
from app.crud.users import r_create_user, r_read_users, r_read_user, r_update_user, r_delete_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep):
    return r_create_user(user, session)


@router.get("/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return r_read_users(session, offset, limit)


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    return r_read_user(user_id, session)


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    return r_update_user(user_id, user, session)


@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    return r_delete_user(user_id, session)
