from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    email: str

    class config():
        orm_mode = True