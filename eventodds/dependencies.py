# this files is for get_db , get_current_user and similar common operation section
from eventodds.config import settings
from eventodds.db.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    async with async_session() as session:
        yield session

