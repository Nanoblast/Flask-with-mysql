from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root@localhost/CRUD")

Base = declarative_base()

class DataModel(Base):
    __tablename__ = 'practice_data'
    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    description = Column(String(255))

Base.metadata.create_all(engine)
