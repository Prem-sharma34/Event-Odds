# this files is for configuration related settings like database url , secret key , etc

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()




class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int





    class Config:
        env_file = ".env"


settings = Settings()