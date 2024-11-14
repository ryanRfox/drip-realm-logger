from datetime import datetime
from typing import Optional
from typing_extensions import TypedDict
from sqlalchemy import JSON, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class DripLogDict(TypedDict):
    event_type: str
    timestamp: datetime
    subscriber_id: str
    data: dict

class DripLog(Base):
    __tablename__ = "drip_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    subscriber_id: Mapped[str] = mapped_column(String)
    data: Mapped[dict] = mapped_column(JSON)

class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    realm_id: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    event_type: Mapped[str] = mapped_column(String)
    guild_id: Mapped[str] = mapped_column(String)
    receiver: Mapped[str] = mapped_column(String)
    sender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Store data in a more structured way
    activity: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    receiver_balance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sender_balance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Keep original JSON for reference
    raw_data: Mapped[dict] = mapped_column(JSON) 