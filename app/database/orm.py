
from sqlalchemy import text, insert, select, inspect, and_, func, cast, Integer, or_, delete, update

from app.database.database_f import sync_engine, async_engine, session_factory, async_session_factory
from app.database.models import User, Base, UserProfile
from app.database.schemas import UsersDTO, ProfilesDTO


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
            query = (
                select(User)
                .order_by(User.id.desc())
                .limit(1)
            )
            result = await session.execute(query)
            result_orm = result.scalars().all()
            result_dto = [UsersDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def insert_profiles(name: str, age: int, birthday: str, zodiac: str, group: str, hobbies: str, contact: str,
                              photo_id: str, user_id: int):
        async with async_session_factory() as session:
            profile1 = UserProfile(name=name, age=age, birthday=birthday, zodiac=zodiac, group=group,
                                   hobbies=hobbies, contact=contact, photo_id=photo_id, user_id=user_id)
            # profile2 = UserProfile(id=39, name="", age=, ="",
            #                              group="", hobbies="",
            #                              contact="@", user_id=)

            session.add_all([profile1])
            await session.commit()

    @staticmethod
    async def send_user_profile(tg_id: str):
        async with async_session_factory() as session:
            query = (
                select(UserProfile).where(UserProfile.contact.in_([f"{tg_id}"]))
                # select(UserProfile).where(UserProfile.contact == tg_id)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def convert_users_to_dto():
        async with async_session_factory() as session:
            query = (
                select(UserProfile)
                .order_by(func.random())
                .limit(1)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def delete_profile(tg_id: str):
        async with async_session_factory() as session:
            stmt = delete(User).where(User.tg_id == tg_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_photo(tg_id: str, photo_id: str):
        async with async_session_factory() as session:
            stmt = (
                update(UserProfile).
                where(UserProfile.contact == tg_id).
                values(photo_id=photo_id)
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def update_hobby(tg_id: str, hobbies: str):
        async with async_session_factory() as session:
            stmt = (
                update(UserProfile)
                .where(UserProfile.contact == tg_id)
                .values(hobbies=hobbies)
            )

            await session.execute(stmt)
            await session.commit()

