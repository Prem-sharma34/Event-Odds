from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from eventodds.config import settings

engine = create_async_engine(settings.DATABASE_URL)

# expire_on_commit=False so ORM objects stay readable after a commit,
# which matters when a response is serialised after the session commits.
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession, 
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass
