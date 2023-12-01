from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from envs.db_secrets import db_url
from src.database.db_orm import User, UserLogInfo, AssetUpdates


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


async def get_all_users_id():
    async with async_session() as session:
        user = await session.execute(
            select(User.user_id)
        )
        users_ids = user.all()
        users_ids = [user_id[0] for user_id in users_ids]
        return users_ids


async def create_new_user(user_id, user_name, subscribes):
    async with async_session() as session:
        new_user = User(user_id=user_id, user_name=user_name, subscribes=subscribes)
        session.add(new_user)
        await session.commit()


async def update_user_subs(user_id, new_subscribes):
    async with async_session() as session:
        user = await session.execute(
            select(User).filter(User.user_id == user_id)
        )
        user_to_update = user.scalar_one_or_none()
        new_log = UserLogInfo(
            user_id=user_id,
            subscribes_before=user_to_update.subscribes,
            subscribes_after=new_subscribes
        )
        user_to_update.subscribes = new_subscribes
        await session.commit()
        session.add(new_log)
        await session.commit()


async def add_new_asset_info(asset_update_info):
    async with async_session() as session:
        new_asset_info = AssetUpdates(
            asset_name=asset_update_info['asset_name'],
            n_buy=asset_update_info['n_buy'],
            n_sell=asset_update_info['n_sell'],
            n_neutral=asset_update_info['n_neutral'],
            recommendation=asset_update_info['recommendation'],
            open_price=asset_update_info['open_price'],
            close_price=asset_update_info['close_price'],
            low_price=asset_update_info['low_price'],
            high_price=asset_update_info['high_price'],
            update_date=asset_update_info['update_date'],
        )
        session.add(new_asset_info)
        await session.commit()


async def get_last_asset_info(asset_name):
    async with async_session() as session:
        asset_info = await session.execute(
            select(AssetUpdates).filter(AssetUpdates.asset_name == asset_name).
                order_by(AssetUpdates.update_id.desc()).limit(1)
        )
        asset_info = asset_info.scalar_one_or_none()
        if asset_info:
            return asset_info
        else:
            raise ValueError
