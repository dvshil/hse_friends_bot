
from sqlalchemy import text, insert, select, inspect, and_, func, cast, Integer, or_

from app.database.database_f import sync_engine, async_engine, session_factory, async_session_factory
from app.database.models import User, Base, UserProfile



class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        # Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True





class AsyncORM:
    @staticmethod
    async def insert_users(intg_id: str):
        async with async_session_factory() as session:
            user1 = User(tg_id=intg_id)  # RETURNING id
            # tg_user2 = User(id=, tg_id="")
            # tg_user3 = User(id=36, tg_id="")
            # tg_user4 = User(id=37, tg_id="@")
            session.add_all([user1])

            # await session.flush()
            await session.commit()