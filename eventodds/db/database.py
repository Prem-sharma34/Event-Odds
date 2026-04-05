import os
from sqlalchemy.orm import DeclarativeBase , sessionmaker
from eventodds.config import settings


class Base(DeclarativeBase):
    pass


