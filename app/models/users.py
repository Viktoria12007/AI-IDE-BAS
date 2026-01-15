from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from pydantic import EmailStr


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )


class UserCreate(SQLModel):
    username: str
    email: EmailStr
    password: str


class User(TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field()


class UserPublic(TimestampMixin):
    id: int
    username: str
    password: str


class UserUpdate(UserCreate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
