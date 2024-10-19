
import datetime
from typing import Optional, Annotated

from sqlalchemy import String, MetaData, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database_f import Base, str_200



intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.utcnow,)]




class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[str]


class UserProfile(Base):
    __tablename__ = 'profiles'

    id: Mapped[intpk]
    name: Mapped[str_200]
    age: Mapped[int]
    birthday: Mapped[str_200]
    zodiac: Mapped[Optional[str]]
    group: Mapped[str_200]
    hobbies: Mapped[str] = mapped_column(String(350))
    contact: Mapped[str_200]
    photo_id: Mapped[str_200]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]