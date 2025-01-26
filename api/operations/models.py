from sqlalchemy import Column, Integer, String, Float, DateTime
from api.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    articul = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    total_quantity = Column(Integer)


class Job(Base):
    __tablename__ = 'apscheduler_jobs'
    id = Column(String, primary_key=True)
    next_run_time = Column(DateTime(timezone=True))
    job_state = Column(String)
