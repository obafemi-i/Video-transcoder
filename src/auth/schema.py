from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    email: str

    class config():
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # email: str | None = None
    email: Optional[str] = None
