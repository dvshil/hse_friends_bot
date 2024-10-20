import asyncio
from typing import Annotated

from sqlalchemy import URL, create_engine, text, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

DATABASE_URL_asyncpg = "postgresql+asyncpg://postgres:hsefriends76@localhost/practicedb"
DATABASE_URL_psycopg = "postgresql+psycopg://postgres:hsefriends76@localhost/practicedb"


sync_engine = create_engine(url=DATABASE_URL_psycopg,
                       echo=True,

)


async_engine = create_async_engine(url=DATABASE_URL_asyncpg,
                       echo=True,

)


session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)


str_200 = Annotated[str, 200]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_200: String(200)
    }

    repr_cols_num = 10
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
