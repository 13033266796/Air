from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, DECIMAL, Integer, VARCHAR, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LatestAirInfo(Base):
    __tablename__ = "display_app_latestairinfo"
    id   = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(VARCHAR(10), nullable=False)
    city_date = Column(DATETIME, nullable=False)
    city_AQI = Column(DECIMAL(18), nullable=False)
    city_PM2_5 = Column(DECIMAL(18), nullable=False)

class PredictAirInfo(Base):
    __tablename__ = "display_app_predictinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(VARCHAR(10), nullable=False)
    city_date = Column(DATETIME, nullable=False)
    city_AQI = Column(DECIMAL(18), nullable=False)
    city_PM2_5 = Column(DECIMAL(18), nullable=False)

class AirInfo(Base):
    __tablename__ = "display_app_airinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(VARCHAR(10), nullable=False)
    city_date = Column(DATETIME, nullable=False)
    city_AQI = Column(DECIMAL(18), nullable=False)
    city_PM2_5 = Column(DECIMAL(18), nullable=False)

engine = create_engine("mysql+pymysql://root:123456@47.115.24.101/air_dev")
Session = sessionmaker(bind=engine)
session = Session()

def get_mysql_db():
    """ 获取操作mysql的session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class MysqlModel(object):

    def __init__(self):
        self._db = None

    def __enter__(self):
        self._db = get_mysql_db()
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.commit()
        self._db.close()