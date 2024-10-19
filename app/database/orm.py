
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