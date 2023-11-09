from sqlalchemy import create_engine, Integer, String, Column

from sqlalchemy.orm import declarative_base
from envs.db_secrets import db_url
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True)
    user_name = Column(String(100), nullable=False)


if __name__ == '__main__':
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)



