from pydantic import BaseModel

class RegisterUserModel(BaseModel):
    username: str
    email: str
    password: str