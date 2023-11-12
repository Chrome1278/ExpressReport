from sqlalchemy import create_engine, Integer, String, Column, ARRAY, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.orm import declarative_base
from envs.db_secrets import db_url


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(100), nullable=False)
    create_date = Column(DateTime(), nullable=False)
    subscribes = Column(ARRAY(Boolean), nullable=False)
    user_log_info = relationship('user_log_info')


class UserLogInfo(Base):
    __tablename__ = 'user_log_info'
    log_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("user.user_id"), nullable=False)
    subscribes_before = Column(ARRAY(Boolean), nullable=False)
    subscribes_after = Column(ARRAY(Boolean), nullable=False)
    change_date = Column(DateTime(), nullable=False)


if __name__ == '__main__':
    engine = create_engine(db_url)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



