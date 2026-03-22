from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column , Integer , String , Enum , DateTime , Boolean , Text
import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine , MetaData , ForeignKey ,UniqueConstraint
from sqlalchemy.sql import func

load_dotenv()

database_url = os.getenv('postgres_url')

engine = create_engine(database_url)

meta = MetaData()


class Base(DeclarativeBase):
    pass

# -- Enums
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

    id = Column(UUID(as_uuid=True), primary_key=True , default=uuid.uuid4)
    name = Column(String(50))
    email = Column(String(50) , unique=True ,nullable=False)
    password_hash = Column(String(100))
    role = Column(Enum(UserRole) , default=UserRole.user)
    create_at = Column(DateTime(timezone=True), nullable=False)

class Events(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True , default=uuid.uuid4)
    organizer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String(50))
    description = Column(Text)
    type = Column(Enum(EventType) , default=EventType.public,nullable=False)
    status = Column(Enum(EventStatus) , default=EventStatus.upcoming,nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True) , nullable=False)
    create_at = Column(DateTime(timezone=True),server_default=func.now() , nullable=False)




class Participants(Base):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True , default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id') , nullable=False)
    name = Column(String(50) , nullable=False)
    vote_count = Column(Integer,default=0 , nullable=False)
    is_approved = Column(Boolean , default=False , nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now() ,nullable=False)




class Predictions(Base):
    __tablename__ = 'predictions'

    id = Column(UUID(as_uuid=True), primary_key=True )
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id') )
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id') )
    participant_id = Column(UUID(as_uuid=True), ForeignKey('participants.id'))
    created_at = Column(DateTime(timezone=True),nullable=False)



    __table_args__ = (
        UniqueConstraint('user_id' , 'event_id' , name = 'one_vote_per_user_per_event')
    )