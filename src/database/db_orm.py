from sqlalchemy import create_engine, Integer, String, Column, ARRAY, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import create_database, drop_database
from sqlalchemy.orm import declarative_base
from envs.db_secrets import db_url_old
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(100), nullable=False)
    create_date = Column(DateTime(), nullable=False, server_default=func.now())
    subscribes = Column(ARRAY(Boolean), nullable=False)
    user_log_info = relationship('UserLogInfo')


class UserLogInfo(Base):
    __tablename__ = 'user_log_info'
    log_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("user.user_id"), nullable=False)
    subscribes_before = Column(ARRAY(Boolean), nullable=False)
    subscribes_after = Column(ARRAY(Boolean), nullable=False)
    change_date = Column(DateTime(), nullable=False, server_default=func.now())


class AssetUpdates(Base):
    __tablename__ = 'asset_update'
    update_id = Column(Integer(), primary_key=True)
    asset_name = Column(String(32), nullable=False)
    n_buy = Column(Integer(), nullable=False)
    n_sell = Column(Integer(), nullable=False)
    n_neutral = Column(Integer(), nullable=False)
    recommendation = Column(String(32), nullable=False)
    open_price = Column(Integer(), nullable=False)
    close_price = Column(Integer(), nullable=False)
    low_price = Column(Integer(), nullable=False)
    high_price = Column(Integer(), nullable=False)
    update_date = Column(DateTime(), nullable=False, server_default=func.now())


if __name__ == '__main__':
    engine = create_engine(db_url_old)
    # drop_database(engine.url)
    # create_database(engine.url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
