from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SAEnum
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os
import enum
import uuid
from sqlalchemy import create_engine

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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)           # no unique=True
    role = Column(SAEnum(UserRole), default=UserRole.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Events(Base):
    __tablename__ = 'events'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(SAEnum(EventType), default=EventType.public, nullable=False)
    status = Column(SAEnum(EventStatus), default=EventStatus.upcoming, nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Participants(Base):
    __tablename__ = 'participants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
    name = Column(String(100), nullable=False)
    vote_count = Column(Integer, default=0, nullable=False)       # default=0, not NULL
    is_approved = Column(Boolean, default=False, nullable=False)  # Boolean type, not bool
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Predictions(Base):
    __tablename__ = 'predictions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'), nullable=False)
    participant_id = Column(UUID(as_uuid=True), ForeignKey('participants.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name='uq_one_vote_per_user_per_event'),
    )