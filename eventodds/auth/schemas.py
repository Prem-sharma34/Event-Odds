# this files is for authentication related schemas like register/login/logout

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None


