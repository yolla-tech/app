from pydantic import BaseModel


class LoginUserModel(BaseModel):
    username: str
    email: str
    password: str