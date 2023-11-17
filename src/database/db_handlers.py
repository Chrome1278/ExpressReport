from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from envs.db_secrets import db_url
from src.database.db_orm import User


engine = create_async_engine(db_url)
async_session = sessionmaker(engine, class_=AsyncSession)


async def is_new_user(user_id):
    async with async_session() as session:
        user = await session.execute(
            select(User).filter(User.user_id == user_id)
        )
        user = user.scalar_one_or_none()
        if user:
            return False
        else:
            return True


async def get_user_subscribes(user_id):
    async with async_session() as session:
        user = await session.execute(
            select(User.subscribes).filter(User.user_id == user_id)
        )
        subscribes = user.scalar()
        return subscribes


async def create_new_user(user_id, user_name, subscribes):
    async with async_session() as session:
        new_user = User(user_id=user_id, user_name=user_name, subscribes=subscribes)
        session.add(new_user)
        await session.commit()
