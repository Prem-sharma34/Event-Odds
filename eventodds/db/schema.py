from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship 
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from dotenv import load_dotenv
from typing import Optional
import os
import enum
import uuid
from sqlalchemy import create_engine
from datetime import datetime


load_dotenv()
database_url = os.getenv('postgres_url')
engine = create_engine(database_url)


class Base(DeclarativeBase):
    pass



# --- Enums ---

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"
    organizer = "organizer"
    participant = "participant"


class EventType(enum.Enum):
    public = "public"
    private = "private"


class EventStatus(enum.Enum):
    upcoming = "upcoming"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


# --- Models ---

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.user)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationships — navigate without writing JOINs
    events: Mapped[list["Events"]] = relationship(back_populates="organizer")
    predictions: Mapped[list["Predictions"]] = relationship(back_populates="user")


class Events(Base):
    __tablename__ = 'events'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)       # Optional = nullable
    type: Mapped[EventType] = mapped_column(SAEnum(EventType), default=EventType.public)
    status: Mapped[EventStatus] = mapped_column(SAEnum(EventStatus), default=EventStatus.upcoming)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationships
    organizer: Mapped["Users"] = relationship(back_populates="events")
    participants: Mapped[list["Participants"]] = relationship(back_populates="event")
    predictions: Mapped[list["Predictions"]] = relationship(back_populates="event")


class Participants(Base):
    __tablename__ = 'participants'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('events.id'))
    name: Mapped[str] = mapped_column(String(100))
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # relationships
    event: Mapped["Events"] = relationship(back_populates="participants")
    predictions: Mapped[list["Predictions"]] = relationship(back_populates="participant")


class Predictions(Base):
    __tablename__ = 'predictions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('events.id'))
    participant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('participants.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_one_vote_per_user_per_event'),
    )

    # relationships
    user: Mapped["Users"] = relationship(back_populates="predictions")
    event: Mapped["Events"] = relationship(back_populates="predictions")
    participant: Mapped["Participants"] = relationship(back_populates="predictions")