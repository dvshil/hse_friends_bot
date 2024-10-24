
from sqlalchemy import text, insert, select, inspect, and_, func, cast, Integer, or_, delete, update

from app.database.database_f import sync_engine, async_engine, session_factory, async_session_factory
from app.database.models import Base, UserProfile, UserLikes
from app.database.schemas import UsersDTO, ProfilesDTO, LikesDTO


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = True
        # Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True





class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

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
    async def delete_profile(user_id: int):
        async with async_session_factory() as session:
            stmt = delete(UserProfile).where(UserProfile.user_id == user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def send_user_profile(user_id: int):
        async with async_session_factory() as session:

            query = (
                select(UserProfile).where(UserProfile.user_id.in_(user_id))
                # select(UserProfile).where(UserProfile.contact == tg_id)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def convert_users_to_dto(user_id: int):
        async with async_session_factory() as session:
            # shown_ids = set()
            query = (
                select(UserProfile)
                .filter((UserProfile.user_id != user_id))
                .order_by(func.random())
                .limit(1)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()

            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    # PART 1
    @staticmethod
    async def getting_pk(user_id: int):
        async with async_session_factory() as session:
            query = (
                select(UserProfile)
                .where(UserProfile.user_id == user_id)
            )
            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    # PART 2
    @staticmethod
    async def getting_like_id(pk: int):
        async with async_session_factory() as session:
            query = (
                select(UserLikes)
                .where(UserLikes.profile_id == pk)

            )
            res = await session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [LikesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    # PART 3
    @staticmethod
    async def convert_likes_to_dto(like_id: int):
        async with async_session_factory() as session:
            query = (
                select(UserProfile)
                .where(UserProfile.user_id == like_id)
            )

            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [ProfilesDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def remove_one_like(pk: int, user_id: int):
        async with async_session_factory() as session:
            stmt = delete(UserLikes).where(UserLikes.profile_id == pk
                                           and UserLikes.like_id == user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def remove_all_likes(pk: int):
        async with async_session_factory() as session:
            stmt = delete(UserLikes).where(UserLikes.profile_id == pk)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def insert_likes(like_id: int, pk: int):
        async with async_session_factory() as session:
            like_1 = UserLikes(like_id=like_id, profile_id=pk)

            session.add_all([like_1])

            await session.commit()


    # @staticmethod
    # async def delete_profile(tg_id: str):
    #     async with async_session_factory() as session:
    #         stmt = delete(User).where(User.tg_id == tg_id)
    #         await session.execute(stmt)
    #         await session.commit()

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
