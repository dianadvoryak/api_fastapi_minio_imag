from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str
