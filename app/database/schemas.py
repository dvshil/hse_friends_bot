from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict




class UsersAddDTO(BaseModel):
    tg_id: str

class UsersDTO(UsersAddDTO):
    id: int

class ProfilesAddDTO(BaseModel):
    name: str
    age: int
    birthday: str
    zodiac: str
    group: str
    hobbies: str
    contact: str
    photo_id: str
    user_id: int

class ProfilesDTO(ProfilesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class ProfilesRelDTO(ProfilesDTO):
    user: "UsersDTO"

class UsersRelDTO(UsersDTO):
    resumes: list["ProfilesDTO"]