from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True)
    realm_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String)
    data = Column(JSON) 